from typing import List
from django.db import models

from .validation import is_config_item_valid
from .settings import SettingsKey


class ConfigItem(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    value = models.TextField(default="", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(default="", null=True, blank=True)

    def clean(self):
        is_config_item_valid(name=self.name, value=self.value)


def get_setting(setting_name: SettingsKey, default=""):
    setting = ConfigItem.objects.filter(name=setting_name.name).first()
    return setting.value if (setting and setting.value) else default


def get_settings(setting_names: List[str]):
    """
    Retrieves settings in a bulk.
    """
    return {
        ci["name"]: ci["value"]
        for ci in ConfigItem.objects.filter(name__in=setting_names).values(
            "name", "value"
        )
    }
