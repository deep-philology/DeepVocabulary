from account.models import Account, EmailAddress
from mozilla_django_oidc.auth import OIDCAuthenticationBackend, default_username_algo


class PinaxOIDCAuthenticationBackend(OIDCAuthenticationBackend):

    def create_user(self, claims):
        """
        Create a user account for the given claims.

        This method is overridden to ensure we create a user account
        which will work in the DUA world.
        """
        username = claims.get("preferred_username", default_username_algo(claims["email"]))
        user = self.UserModel(username=username, email=claims["email"])
        user._disable_account_creation = True
        user.set_unusable_password()
        user.save()
        extra = {}
        if claims.get("zoneinfo"):
            extra["timezone"] = claims["zoneinfo"]
        if claims.get("locale"):
            extra["language"] = claims["locale"]
        Account.create(**{
            "request": self.request,
            "user": user,
            "create_email": False,
            **extra,
        })
        if claims.get("email_verified", False):
            EmailAddress.objects.create(
                user=user,
                email=user.email,
                verified=True,
                primary=True,
            )
        else:
            EmailAddress.objects.add_email(user, user.email, confirm=True)
        return user

    def verify_claims(self, claims):
        checks = set()
        email = claims.get("email")
        if email:
            try:
                email_address = EmailAddress.objects.get(email__iexact=email)
            except EmailAddress.DoesNotExist:
                checks.add(True)
            else:
                # check if the found email address is verified.
                # we need this because if the user has an unverified
                # email address we never get to fail the authentication.
                # however, this is being overly protective because all
                # users who authenticate with OIDC will have a verified
                # email address.
                # @@@ consider creating a django.contrib.messages message
                checks.add(email_address.verified)
        return all(checks)

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
