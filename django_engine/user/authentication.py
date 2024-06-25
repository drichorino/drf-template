from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models.token import BlacklistedAccessToken


class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):        
        # Decode the byte string to a regular string
        decoded_token = raw_token.decode("utf-8")

        if BlacklistedAccessToken.objects.filter(token=decoded_token).exists():
            raise AuthenticationFailed("Session expired, please log in again.")
        return super().get_validated_token(raw_token)
