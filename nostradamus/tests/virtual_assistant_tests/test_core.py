import os

os.environ["DJANGO_SETTINGS_MODULE"] = "nostradamus.settings"

import django
from django.conf import settings

settings.MONGODB_NAME = "testdb"

django.setup()

import unittest
import pytest
import requests

from json import dumps
from apps.extractor.main.connector import DB
from datetime import datetime as dt


@pytest.mark.usefixtures("chatbot_url")
class TestCoreBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.__fill_testdb()

    @classmethod
    def tearDownClass(cls) -> None:
        DB.delete_many({})

    @classmethod
    def __fill_testdb(self):
        DB.insert_many(
            documents=[
                {
                    "Project": "Test Project",
                    "Attachments": 12,
                    "Priority": "Minor",
                    "Created": dt.now(),
                    "Resolved": dt.now(),
                    "Updated": dt.now(),
                    "Labels": "Test Label",
                    "Comments": 1,
                    "Status": "Open",
                    "Key": str(_),
                    "Summary": "Test Summary",
                    "Resolution": "Unresolved",
                    "Description": "Test Description",
                    "Description_tr": "Test Description_tr",
                    "ttr": 10,
                    "Markup": 1,
                    "Components": "Test components",
                    "Version": "Test Version",
                    "Assignee": "Test Assignee",
                    "Reporter": "Test Reporter",
                }
                for _ in range(100)
            ],
            ordered=False,
        )

    def test_default_greeting(self):
        message = {
            "sender": "user",
            "message": "hello",
        }
        request = requests.post(
            self.chatbot_url + "webhook/", data=dumps(message)
        )
        data = request.json()

        assert all(
            [
                data[0]["text"] in ["Hi", "Hello!", "Hey"],
                data[1]["text"] == "I'm a virtual assistant.",
                data[2]["text"] == "How can I help you?",
            ]
        )

    def test_default_what_do_you_can(self):
        message = {"sender": "user", "message": "What do you can?"}

        request = requests.post(
            self.chatbot_url + "webhook/", data=dumps(message)
        )

        assert (
            request.json()[0]["text"]
            == "I can give you the latest news on your project."
        )

    def test_default_what_is_nostradamus(self):
        message = {"sender": "user", "message": "What is Nostradamus?"}

        request = requests.post(
            self.chatbot_url + "webhook/", data=dumps(message)
        )

        assert (
            "Nostradamus is an application for analyzing software defect reports"
            in request.json()[0]["text"]
        )

    def test_report_bug_not_upload(self):
        message = {
            "sender": "user",
            "message": "status report for today please",
        }

        request = requests.post(
            self.chatbot_url + "webhook/", data=dumps(message)
        )
        data = request.json()

        assert (
            data[0]["text"]
            == "Oops! Bugs haven't been uploaded yet. Please try again later"
        )
