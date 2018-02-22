import base64
import hashlib

from django.utils.encoding import force_bytes, smart_text

from account.models import EmailAddress
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


def default_username(email):
    username = base64.urlsafe_b64encode(
        hashlib.sha1(force_bytes(email)).digest()
    )
    return smart_text(username.rstrip(b"="))


class PinaxOIDCAuthenticationBackend(OIDCAuthenticationBackend):

    def create_user(self, claims):
        email = claims["email"]
        username = default_username(email)
        user = self.UserModel.objects.create_user(username, email)
        EmailAddress.objects.create(
            user=user,
            email=email,
            verified=True,
            primary=True,
        )
        return user

    def verify_claims(self, claims):
        email = claims.get("email")
        if email:
            qs = EmailAddress.objects.filter(
                email__iexact=email,
                verified=True,
            )
            return qs.exists()
        return False

    def filter_users_by_claims(self, claims):
        email = claims.get("email")
        if not email:
            return self.UserModel.objects.none()
        try:
            email_address = EmailAddress.objects.get(
                email__iexact=email,
                verified=True,
            )
        except EmailAddress.DoesNotExist:
            return self.UserModel.objects.none()
        else:
            return self.UserModel.objects.filter(pk=email_address.user_id)
