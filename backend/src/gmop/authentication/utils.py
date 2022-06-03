import logging
from datetime import datetime, timedelta, timezone
from secrets import token_hex
from typing import Tuple

from django.urls import reverse

import gmop.core.messages as messages
from gmop.authentication.models import RefreshToken
from gmop.core.models import get_setting
from gmop.core.settings import SettingsKey
from gmop.users.models import User

logger = logging.getLogger("project")


def get_reverse(obj):
    try:
        return reverse(obj)
    except Exception as e:  # NOQA
        logger.error(messages.CANNOT_REVERSE_URL_ERR_MSG.format(e.args[0]))
        raise Exception(messages.CANNOT_REVERSE_URL_ERR_MSG.format(str(obj)))


def get_current_domain(r):
    if acs := get_setting(SettingsKey.SAML_HOST):
        return acs
    return "{scheme}://{host}".format(
        scheme="https" if r.is_secure() else "http", host=r.get_host(),
    )


def generate_refresh_token(
    user: User, refresh_lifetime: int, ip: str
) -> Tuple[str, datetime]:
    refresh_token = token_hex(32)
    now = datetime.now(tz=timezone.utc)
    refresh_expires_at = now + timedelta(seconds=refresh_lifetime)
    RefreshToken.objects.create(
        token=refresh_token, expires_at=refresh_expires_at, user=user, ip=ip
    )

    return refresh_token, refresh_expires_at
