from django.urls import path

from .views import AuthenticationView, RegistrationView

urlpatterns = [
    path("signin/", AuthenticationView.as_view()),
    path("register/", RegistrationView.as_view()),
]
