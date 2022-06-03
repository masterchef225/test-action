import re
from datetime import datetime

from django.core.exceptions import ValidationError


def has_no_invalid_separators(value: str):
    if not value:
        return True
    if " " in value or ";" in value:
        raise ValidationError("Value should not contain whitespaces or semicolons")
    return True


def is_email_list(value: str):
    if not value:
        return True
    for el in value.split(","):
        if not bool(re.match(r"[^@]+@[^@]+\.[^@]+", el)):
            raise ValidationError(f"{el} is not valid email")
    return True


def is_dates_list(value: str):
    if not value:
        return True
    for el in value.split(","):
        try:
            datetime.strptime(el, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(f"{el} is not valid date - expected YYYY-MM-DD")
    return True


def is_config_item_valid(name: str, value: str):
    # TODO: add checking for appropriate settings: emails, dates..
    return True
