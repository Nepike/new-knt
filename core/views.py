from django.contrib import messages
from django.shortcuts import render

from .forms import DemoForm


def demo(request):
    form = DemoForm(request.GET or None)
    submitted = form.cleaned_data if form.is_valid() else None
    if submitted is not None:
        messages.success(request, "Форма прошла валидацию")
    elif form.is_bound:
        messages.error(request, "В форме есть ошибки")
    return render(request, "core/demo.html", {"form": form, "submitted": submitted})
