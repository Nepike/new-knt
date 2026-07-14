from django.shortcuts import redirect
from django.urls import reverse


class MustChangePasswordMiddleware:
    """Пока стоит must_change_password — пускаем только на смену пароля и выход."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and user.must_change_password:
            allowed = {reverse("password_change"), reverse("logout")}
            if request.path not in allowed:
                return redirect("password_change")
        return self.get_response(request)
