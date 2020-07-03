from apps.analysis_and_training.main.statistics import calculate_statistics


CORRECT_RESULT = {
    "Comments": {"minimum": "0", "maximum": "99", "mean": "50", "std": "29"},
    "Attachments": {
        "minimum": "0",
        "maximum": "99",
        "mean": "50",
        "std": "29",
    },
}


def test_statistics_result(statistics):
    result = calculate_statistics(statistics, ["Comments", "Attachments"])

    assert result == CORRECT_RESULT
