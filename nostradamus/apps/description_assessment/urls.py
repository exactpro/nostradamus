from django.urls import path

from .views import DescriptionAssessment, Predictor, Highlighting

urlpatterns = [
    path("", DescriptionAssessment.as_view()),
    path("predict/", Predictor.as_view()),
    path("highlight/", Highlighting.as_view()),
]
