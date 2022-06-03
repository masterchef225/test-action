from contextlib import suppress
from datetime import datetime, timezone
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, exceptions
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

import gmop.core.messages as messages
from gmop.authentication.jwt import create_token
from gmop.authentication.models import RefreshToken
from gmop.authentication.utils import generate_refresh_token
from gmop.core.models import get_setting
from gmop.core.audit_trail import audit_log_info
from gmop.core.settings import SettingsKey


@swagger_auto_schema(
    method="post",
    responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access_token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="string"
                ),
                "refresh_token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="string"
                ),
                "expires_at": openapi.Schema(
                    type=openapi.FORMAT_DATETIME, description="datetime"
                ),
            },
        )
    },
)
@api_view(["POST"])
@permission_classes([])
def obtain_jwt_token(request):
    if not request.user:
        raise exceptions.AuthenticationFailed(messages.INVALID_CREDENTIALS_ERR_MSG)
    ip = get_ip(request)
    return build_token_response(request.user, ip)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "refresh_token": openapi.Schema(
                type=openapi.TYPE_STRING, description="string"
            ),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access_token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="string"
                ),
                "refresh_token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="string"
                ),
                "expires_at": openapi.Schema(
                    type=openapi.FORMAT_DATETIME, description="datetime"
                ),
            },
        )
    },
)
@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def refresh_jwt_token(request):
    if not (token := request.data.get("refresh_token")):
        raise ValidationError(detail={"refresh_token": "This field is required."})
    ip = get_ip(request)

    try:
        refresh_token = RefreshToken.objects.get(token=token, ip=ip)
        refresh_token.delete()
    except RefreshToken.DoesNotExist:
        with suppress(RefreshToken.DoesNotExist):
            RefreshToken.objects.get(token=token).delete()
        raise exceptions.AuthenticationFailed(messages.CANNOT_REFRESH_TOKEN_ERR_MSG)

    if refresh_token.expires_at > datetime.now(tz=timezone.utc):
        user = refresh_token.user
        return build_token_response(user, ip)
    raise exceptions.AuthenticationFailed(messages.CANNOT_REFRESH_TOKEN_ERR_MSG)


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def build_token_response(user, ip):
    jwt = create_token(
        username=f"{user.first_name} {user.last_name}",
        email=user.email,
        company=user.company,
        access_group=user.access_group,
        ttl_seconds=int(get_setting(SettingsKey.JWT_AUTH_TOKEN_DURATION)),
        secret_key=settings.SECRET_KEY,
    )
    refresh_token, expires_at = generate_refresh_token(
        user=user,
        refresh_lifetime=int(get_setting(SettingsKey.JWT_REFRESH_TOKEN_DURATION)),
        ip=ip,
    )

    audit_log_info(
        username=user.email,
        event=messages.USER_LOGGED_IN_MSG.format(
            ip_address=ip, token=f"******{jwt[-6:]}"
        ),
    )

    return Response(
        data={
            "access_token": jwt,
            "refresh_token": refresh_token,
            "expires_at": expires_at,
        },
        status=status.HTTP_200_OK,
    )
