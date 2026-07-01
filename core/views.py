from django.shortcuts import render

from .forms import DemoForm


def demo(request):
    form = DemoForm(request.GET or None)
    submitted = form.cleaned_data if form.is_valid() else None
    return render(request, "core/demo.html", {"form": form, "submitted": submitted})
