from django.urls import path

from .views import (
    AnalysisAndTrainingView,
    FilterView,
    DefectSubmissionView,
    SignificantTermsView,
    FrequentlyTermsView,
    StatisticsView,
    StatusView,
)


urlpatterns = [
    path("", AnalysisAndTrainingView.as_view()),
    path("filter/", FilterView.as_view()),
    path("defect_submission/", DefectSubmissionView.as_view()),
    path("significant_terms/", SignificantTermsView.as_view()),
    path("frequently_terms/", FrequentlyTermsView.as_view()),
    path("statistics/", StatisticsView.as_view()),
    path("status/", StatusView.as_view()),
]
