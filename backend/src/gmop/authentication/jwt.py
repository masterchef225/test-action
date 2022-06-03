import jwt
from datetime import datetime, timedelta
from rest_framework import exceptions


def create_token(username, email, company, access_group, ttl_seconds, secret_key):
    if (
        not username
        or not email
        or not company
        or not access_group
        or not ttl_seconds
        or ttl_seconds < 0
        or not secret_key
    ):
        raise ValueError

    now = datetime.now()
    dt = now + timedelta(seconds=ttl_seconds)
    jwt_token = jwt.encode(
        {
            "username": username,
            "email": email,
            "company": company,
            "access_group": access_group,
            "iat": int(now.strftime("%s")),
            "exp": int(dt.strftime("%s")),
        },
        secret_key,
        algorithm="HS256",
    )

    return jwt_token.decode("utf-8")
