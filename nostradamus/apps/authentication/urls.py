from django.urls import path

from .views import AuthenticationView, RegistrationView, TestSocketView

urlpatterns = [
    path("signin/", AuthenticationView.as_view()),
    path("register/", RegistrationView.as_view()),
]
