from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.UserRegisterView.as_view()),
    path('activate-account/', views.ActivateAccountView.as_view()),
    path('send-otp/', views.SendOtpView.as_view()),
]
