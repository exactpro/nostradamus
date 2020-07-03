"""nostradamus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(title="Nostradamus API", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0),),
    path("admin/", admin.site.urls),
    path("analysis_and_training/", include("apps.analysis_and_training.urls")),
    path("auth/", include("apps.authentication.urls")),
    path("settings/", include("apps.settings.urls")),
    path(
        "description_assessment/", include("apps.description_assessment.urls")
    ),
    path("qa_metrics/", include("apps.qa_metrics.urls")),
    path("virtual_assistant/", include("apps.virtual_assistant.urls")),
    path("token/verify/", TokenVerifyView.as_view()),
] + staticfiles_urlpatterns()
