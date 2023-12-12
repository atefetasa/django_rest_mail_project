from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('sign-up/', views.UserRegisterView.as_view()),
    path('activate-account/', views.ActivateAccountView.as_view()),
    path('send-otp/', views.SendOtpView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
