from django.urls import path

from apps.virtual_assistant.views import (
    ReportDownloadView,
    ReportCreatorView,
    RequestValuesView,
    IssuesCheckerView,
)

urlpatterns = [
    path("reports/<str:filename>", ReportDownloadView.as_view()),
    path("generate_report/", ReportCreatorView.as_view()),
    path("request_values/", RequestValuesView.as_view()),
    path("issues_checker/", IssuesCheckerView.as_view()),
]
