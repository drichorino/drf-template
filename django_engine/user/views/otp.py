import qrcode
import io
import urllib.parse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status
from django.http import HttpResponse
from utils.responses import success_response, error_response


class Setup2FAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Check if user already has a confirmed TOTP device
        if TOTPDevice.objects.filter(user=request.user, confirmed=True).exists():
            return error_response(
                message="User already has a confirmed TOTP device.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        
        # Create a new TOTP device if no confirmed device exists
        otp_device, created = TOTPDevice.objects.get_or_create(user=request.user, confirmed=False)
        if not created:
            otp_device.delete()
            otp_device = TOTPDevice.objects.create(user=request.user, confirmed=False)
        
        return success_response(
            message="2FA setup initiated. Scan the QR code.",
            status_code=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        user = request.user
        otp_devices = TOTPDevice.objects.filter(user=user)
        if otp_devices.exists():
            otp_devices.delete()
            return success_response(
                message="All TOTP devices have been deleted.",
                status_code=status.HTTP_200_OK,
            )
        else:
            return error_response(
                message="No TOTP devices found to delete.",
                status_code=status.HTTP_404_NOT_FOUND,
            )


class QRCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        otp_device = user.totpdevice_set.filter(confirmed=False).first()
        if not otp_device:
            return error_response(
                message="2FA setup not initiated.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Generate QR code
        qr_url = otp_device.config_url

        parsed_url = urllib.parse.urlparse(qr_url)
        existing_params = urllib.parse.parse_qs(parsed_url.query)

        issuer = settings.SITE_ABBRV
        account_name = user.email

        modified_path = f"{issuer}:{urllib.parse.quote(account_name)}"

        existing_params["issuer"] = issuer
        modified_query = urllib.parse.urlencode(existing_params, doseq=True)

        modified_url = urllib.parse.urlunparse(
            parsed_url._replace(path=modified_path, query=modified_query)
        )

        qr = qrcode.make(modified_url)
        stream = io.BytesIO()
        qr.save(stream, "PNG")
        stream.seek(0)
        return HttpResponse(stream, content_type="image/png")


class Confirm2FAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        otp_device = request.user.totpdevice_set.filter(confirmed=False).first()
        if otp_device.verify_token(token):
            otp_device.confirmed = True
            otp_device.save()
            return success_response(
                message="2FA setup complete.", status_code=status.HTTP_200_OK
            )
        else:
            return error_response(
                message="Invalid token.", status_code=status.HTTP_400_BAD_REQUEST
            )
