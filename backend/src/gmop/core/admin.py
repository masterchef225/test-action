from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import admin as auth_admin
from django.forms import TextInput
from gmop.users.models import User

from .models import ConfigItem

admin.site.site_header = "GMOP administration"


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    list_display = (
        "first_name",
        "last_name",
        "email",
        "company",
        "access_group",
        "is_active",
        "is_superuser",
    )

    fields = (
        "email",
        "password",
        "first_name",
        "last_name",
        "company",
        "access_group",
        "is_active",
        "is_superuser",
    )

    fieldsets = None

    readonly_fields = (
        "first_name",
        "last_name",
        "email",
        "company",
        "access_group",
        "is_active",
    )

    list_filter = (
        "is_superuser",
        "company",
        "access_group",
    )

    search_fields = ("first_name", "last_name", "email")

    ordering = ("email",)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(ConfigItem)
class ConfigItemAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "description")
    list_editable = ("value",)
    search_fields = ("name",)
    fields = ("name", "value", "description")

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ConfigItemAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        # Display item in one line
        if db_field.name == "value" and "change" not in kwargs["request"].path:
            field.widget = TextInput(attrs={"size": 40})
        return field


admin.site.unregister(Group)
