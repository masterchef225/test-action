import base64
import logging
from django.contrib.auth import get_user_model
from rest_framework import exceptions, authentication
from gmop.core.settings import SettingsKey
from gmop.core.models import get_setting
import gmop.core.messages as messages

logger = logging.getLogger("project")

UserModel = get_user_model()


class SSOAuthBackend(authentication.BaseAuthentication):
    authentication_header_prefix = "basic"

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or len(auth_header) < 2:
            logger.debug("No auth header provided: proceed to next auth method")
            return None

        prefix = auth_header[0].decode("utf-8")
        credentials = auth_header[1].decode("utf-8")

        if not prefix.lower() == self.authentication_header_prefix:
            logger.error("No basic auth header provided: proceed to next auth method")
            return None

        try:
            username, password = (
                base64.b64decode(credentials).decode("utf-8").split(":")
            )
        except Exception as e:
            logger.error("Cannot decode credentials: {}", e)
            raise exceptions.AuthenticationFailed

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            raise exceptions.ValidationError(messages.LOGIN_INFORMATION_IS_INCORRECT)

        if not user.is_active:
            raise exceptions.ValidationError(messages.AUTH_FAILED_LOGIN_IS_INACTIVE)

        if user.company in get_setting(SettingsKey.NOT_SSO_AUTH_COMPANIES):
            logger.debug("It is not SSO user: proceed to next auth method")
            return None

        # TODO: some realization checking SSO authentication and return user

        return None, None
