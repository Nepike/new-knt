from django import forms
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import Group

from core.widgets import AccentSelect, AccentSelectMultiple

from .models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name", "surname")


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


def grantable_groups(user):
    """Группы, которые user может выдавать: их права не шире его собственных."""
    if user.is_superuser:
        return Group.objects.all()
    mine = user.get_all_permissions()
    ids = [
        g.id
        for g in Group.objects.prefetch_related("permissions__content_type")
        if {f"{p.content_type.app_label}.{p.codename}" for p in g.permissions.all()} <= mine
    ]
    return Group.objects.filter(id__in=ids)


class RegisterUserForm(forms.ModelForm):
    """Регистрация пользователя: пароль не задаётся — уходит письмо со ссылкой.
    Роли (группы) без выбора = обычный студент."""

    class Meta:
        model = User
        fields = ("name", "surname", "patronymic", "email", "team", "groups")
        labels = {"groups": "Роли"}
        help_texts = {"groups": ""}
        widgets = {"team": AccentSelect(search=True), "groups": AccentSelectMultiple}

    def __init__(self, *args, creator=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["groups"].queryset = grantable_groups(creator) if creator else Group.objects.none()
