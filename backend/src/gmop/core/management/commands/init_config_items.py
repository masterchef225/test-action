from django.core.management.base import BaseCommand

from gmop.core.models import ConfigItem
from gmop.core.settings import SettingsKey

SUCCESS_MSG = "{created_count} config items was added, {updated_count} was updated"


class Command(BaseCommand):
    help = "This command initialize all config items in database"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0
        for key in SettingsKey:
            config_item, created = ConfigItem.objects.get_or_create(
                name=key.name, defaults={"value": "", "description": key.value}
            )
            if created:
                created_count += 1
            else:
                if config_item.description != key.value:
                    config_item.description = key.value
                    config_item.save()
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                SUCCESS_MSG.format(
                    created_count=created_count, updated_count=updated_count
                )
            )
        )
