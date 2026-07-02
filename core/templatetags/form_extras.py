import json

from django import template

register = template.Library()


@register.filter
def widget_type(field):
    """Имя класса виджета поля — чтобы inputs.html выбрал нужную раскладку."""
    return field.field.widget.__class__.__name__


@register.filter
def select_json(field):
    """options/selected для наших селектов (Alpine). JSON готовим в Python, не в шаблоне."""
    options = [
        {"value": str(v), "label": str(label)}
        for v, label in field.field.choices
        if v not in ("", None)
    ]
    value = field.value()
    if value is None:
        selected = []
    elif isinstance(value, (list, tuple)):
        selected = [str(v) for v in value]
    else:
        selected = [str(value)]
    return {
        "options": json.dumps(options, ensure_ascii=False),
        "selected": json.dumps(selected, ensure_ascii=False),
    }
