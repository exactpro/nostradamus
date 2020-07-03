from django.urls import path

from .views import DescriptionAssesment, Predictor, Highlighting

urlpatterns = [
    path("", DescriptionAssesment.as_view()),
    path("predict/", Predictor.as_view()),
    path("highlight/", Highlighting.as_view()),
]
