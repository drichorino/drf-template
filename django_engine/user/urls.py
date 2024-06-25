from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.user import UserViewSet
from .views.auth import AuthView
from .views.otp import Setup2FAView, QRCodeView, Confirm2FAView

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    
    # JWT Tokens
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Login and Logout
    path("auth/", AuthView.as_view(), name="auth"),
    
    # 2FA endpoints
    path("setup-2fa/", Setup2FAView.as_view(), name="setup_2fa"),
    path("qr-code/", QRCodeView.as_view(), name="qr_code"),
    path("confirm-2fa/", Confirm2FAView.as_view(), name="confirm_2fa"),
]
