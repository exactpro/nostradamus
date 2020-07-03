from django.urls import path

from .views import (
    FilterSettingsView,
    QAMetricsSettingsView,
    TrainingSettingsView,
    PredictionsTableSettingsView,
)

urlpatterns = [
    path("filters/", FilterSettingsView.as_view()),
    path("qa_metrics/", QAMetricsSettingsView.as_view()),
    path("predictions_table/", PredictionsTableSettingsView.as_view()),
    path("training/", TrainingSettingsView.as_view()),
]
