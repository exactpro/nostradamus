from django.urls import path

from .views import QAMetricsView, PredictionsTableView, PredictionsInfoView

urlpatterns = [
    path("", QAMetricsView.as_view()),
    path("predictions_info/", PredictionsInfoView.as_view()),
    path("predictions_table/", PredictionsTableView.as_view()),
]
