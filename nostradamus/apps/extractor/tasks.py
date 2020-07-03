from __future__ import absolute_import, unicode_literals
from functools import wraps
from time import sleep

from celery import group
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from kombu import Queue

from nostradamus.celery import app
from utils.redis import redis_conn
from apps.extractor.main.jira_api import JAPI
from apps.extractor.main.connector import (
    get_largest_keys,
    get_issues,
    update_issues,
)


logger = get_task_logger(__name__)

app.conf.task_queues = [
    Queue("celery", queue_arguments={"x-queue-mode": "lazy"}),
]

app.conf.beat_schedule = {
    "extract-new-issues": {
        "task": "apps.extractor.tasks.task_extract_new_issues",
        "schedule": crontab(minute="*/10"),
        "args": (),
    },
    "extract-updated-issues": {
        "task": "apps.extractor.tasks.task_extract_updated_issues",
        "schedule": crontab(minute="*/15"),
        "args": (),
    },
}


def lock_task(timeout=None):
    def task_exc(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret_value = None
            lock_ = False
            lock_id = "celery-single-instance-" + func.__name__
            lock = redis_conn.lock(lock_id, timeout=timeout)

            try:
                lock_ = lock.acquire(blocking=False)
                if lock_:
                    ret_value = func(*args, **kwargs)
            finally:
                if lock_:
                    lock.release()

            return ret_value

        return wrapper

    return task_exc


@app.task(bind=True)
@lock_task(timeout=60 * 3)
def task_extract_updated_issues(self):
    logger.info(f"STARTED: issues updating. Task: {self.request}")
    issues = get_issues(fields=["Key", "Updated"])
    if issues:
        request_args = JAPI().get_update_args(issues)
        tasks = [request_issues.s(jql=args) for args in request_args]
        results = group(*tasks).apply_async()
        while not results.ready():
            sleep(60 * 2)
    logger.info(f"FINISHED: issues updating. Task: {self.request}")


@app.task(bind=True)
@lock_task(timeout=60 * 60)
def task_extract_new_issues(self):
    logger.info(f"STARTED: extracting of new issues. Task: {self.request}")
    issue_keys = get_largest_keys()
    request_args = JAPI().get_extract_args(issue_keys)
    tasks = [request_issues.s(*args) for args in request_args]
    results = group(*tasks).apply_async()
    while not results.ready():
        sleep(60 * 3)
    logger.info(f"FINISHED: extracting of new issues. Task {self.request}")


@app.task(bind=True, default_retry_delay=60 * 3)
def request_issues(self, jql: str, start_ind: int = 0, step_size: int = 50):
    try:
        issues = JAPI().execute_jql(jql, start_ind, step_size)
        issues = JAPI().parse_issues(issues)
        update_issues(issues)
    except Exception:
        logger.warning(f"Retrying request issues. Task: {self.request}")
        self.retry(args=(jql, start_ind, step_size), max_retries=15)
