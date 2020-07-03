from django.urls import path

from apps.virtual_assistant.views import ReportDownloadView, ReportCreatorView

urlpatterns = [
    path("reports/<str:filename>", ReportDownloadView.as_view()),
    path("generate_report/", ReportCreatorView.as_view()),
]
