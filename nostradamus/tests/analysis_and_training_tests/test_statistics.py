from apps.analysis_and_training.main.statistics import calculate_statistics


def test_statistics_without_resolution_unresolved(
    statistics, correct_result_statistics
):
    result = calculate_statistics(
        statistics, ["Comments", "Attachments", "Time to Resolve"]
    )

    assert result == correct_result_statistics


def test_statistics_with_resolution_unresolved_piece(
    statistics_2, correct_result_statistics
):
    result = calculate_statistics(
        statistics_2, ["Comments", "Attachments", "Time to Resolve"]
    )

    corr_result = correct_result_statistics.copy()
    corr_result["Time to Resolve"]["minimum"] = "1"

    assert result == corr_result


def test_statistics_with_resolution_unresolved_all(
    statistics_3, correct_result_statistics
):
    result = calculate_statistics(
        statistics_3, ["Comments", "Attachments", "Time to Resolve"]
    )

    corr_result = correct_result_statistics.copy()
    corr_result["Time to Resolve"] = {
        "minimum": "0",
        "maximum": "0",
        "mean": "0",
        "std": "0",
    }
    assert result == corr_result


def test_statistics_error(statistics, correct_result_statistics):
    statistics.iloc[0] = "None"
    result = calculate_statistics(
        statistics, ["Comments", "Attachments", "Time to Resolve"]
    )

    corr_result = correct_result_statistics.copy()
    for key in corr_result:
        corr_result[key] = {
            "minimum": "0",
            "maximum": "0",
            "mean": "0",
            "std": "0",
        }

    assert result == corr_result
