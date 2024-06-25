from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer
from utils.responses import success_response, error_response
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.signals import user_logged_in
from django.dispatch import Signal
from ..models.token import BlacklistedAccessToken

# Custom signal for logging out
user_logged_out = Signal()

class AuthView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    # Login
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        otp = request.data.get("otp")

        if not username or not password:
            return error_response(
                message="Both username and password are required.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # Check for OTP device
                otp_device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
                if otp_device:
                    if not otp:
                        return error_response(
                            message="OTP token is required.",
                            status_code=status.HTTP_400_BAD_REQUEST,
                        )
                    if not otp_device.verify_token(otp):
                        return error_response(
                            message="Invalid OTP token.",
                            status_code=status.HTTP_400_BAD_REQUEST,
                        )
                
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                serializer = UserSerializer(user)
                response = success_response(
                    data={
                        "refresh": str(refresh),
                        "access": str(access),
                        "user": serializer.data,
                    },
                    message="Successfully logged in.",
                    status_code=status.HTTP_200_OK,
                )

                # Set the JWT tokens in cookies
                response.set_cookie(
                    key="access_token",
                    value=str(access),
                    httponly=True,
                    secure=True,  # Set to True in production
                    samesite="Strict",
                )

                response.set_cookie(
                    key="refresh_token",
                    value=str(refresh),
                    httponly=True,
                    secure=True,  # Set to True in production
                    samesite="Strict",
                )

                # Send the user_logged_in signal
                user_logged_in.send(sender=user.__class__, request=request, user=user)

                return response
            else:
                return error_response(
                    message="This account is inactive.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
        return error_response(
            message="Invalid credentials provided.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Logout
    def delete(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            access_token = request.COOKIES.get("access_token")

            token = RefreshToken(refresh_token)
            token.blacklist()

            if access_token:
                BlacklistedAccessToken.objects.create(token=access_token)

            response = success_response(
                message="Logout successful.", status_code=status.HTTP_200_OK
            )

            # Delete the cookies by setting them to empty values and setting the max age to 0
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

            # Send the user_logged_out signal
            user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)

            return response
        except Exception as e:
            return error_response(
                message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
