from django.urls import path

from .views import (
    FilterSettingsView,
    QAMetricsSettingsView,
    TrainingSettingsView,
    PredictionsTableSettingsView,
    SourceFieldView,
    MarkUpEntitiesView,
    BugResolutionView,
)

urlpatterns = [
    path("filters/", FilterSettingsView.as_view()),
    path("qa_metrics/", QAMetricsSettingsView.as_view()),
    path("predictions_table/", PredictionsTableSettingsView.as_view()),
    path("training/", TrainingSettingsView.as_view()),
    path("training/source_field/", SourceFieldView.as_view()),
    path("training/markup_entities/", MarkUpEntitiesView.as_view()),
    path("training/bug_resolution/", BugResolutionView.as_view()),
]
