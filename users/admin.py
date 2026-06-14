from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ("email", "name", "surname", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "name", "surname")
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личное", {"fields": ("name", "surname", "patronymic", "photo", "birthday",
                               "phone", "vk_page", "tg_page", "team")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "must_change_password",
                              "groups", "user_permissions")}),
        ("Прочее", {"fields": ("mailing_allowed", "note", "last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",),
                "fields": ("email", "name", "surname", "password1", "password2")}),
    )
    readonly_fields = ("last_login",)
