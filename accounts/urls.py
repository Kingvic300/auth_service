from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    ForgotPasswordView,
    ResetPasswordView,
    UserProfileView,
    logout_view
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', logout_view, name='user-logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]