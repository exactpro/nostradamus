from django.urls import path

from .views import (
    QAMetricsView,
    QAMetricsFilterView,
    PredictionsTableView,
    PredictionsInfoView,
)

urlpatterns = [
    path("", QAMetricsView.as_view()),
    path("filter/", QAMetricsFilterView.as_view()),
    path("predictions_info/", PredictionsInfoView.as_view()),
    path("predictions_table/", PredictionsTableView.as_view()),
]
