from django.db import models
from django.db.models import ForeignKey

from gmop.users.models import User


class RefreshToken(models.Model):
    token = models.CharField(max_length=64, null=False, blank=False, unique=True)
    user = ForeignKey(User, on_delete=models.CASCADE)
    expires_at = models.DateTimeField(null=False, blank=False)
    ip = models.CharField(max_length=15, null=False, blank=False)

    class Meta:
        db_table = "auth_refresh_token"
