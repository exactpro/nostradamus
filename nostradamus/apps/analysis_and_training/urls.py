from django.urls import path

from .views import (
    AnalysisAndTraining,
    Filter,
    DefectSubmission,
    SignificantTerms,
    Train,
    FrequentlyTerms,
    Statistics,
)


urlpatterns = [
    path("", AnalysisAndTraining.as_view()),
    path("filter/", Filter.as_view()),
    path("defect_submission/", DefectSubmission.as_view()),
    path("significant_terms/", SignificantTerms.as_view()),
    path("train/", Train.as_view()),
    path("frequently_terms/", FrequentlyTerms.as_view()),
    path("statistics/", Statistics.as_view()),
]
