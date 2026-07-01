import json

from django import forms


class _AccentSelectMixin:
    """Общая логика наших селектов: рендер через один шаблон + передача опций/выбранного в Alpine."""

    template_name = "core/widgets/select.html"

    def __init__(self, *args, search=False, label="", **kwargs):
        self.search = search
        self.label = label
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        w = context["widget"]
        w["search"] = self.search
        w["label"] = self.label
        w["is_multiple"] = self.allow_multiple_selected

        options = []
        for val, label in self.choices:
            if val == "" or val is None:
                continue
            options.append({"value": str(val), "label": str(label)})
        w["options_json"] = json.dumps(options, ensure_ascii=False)

        if value is None:
            selected = []
        elif isinstance(value, (list, tuple)):
            selected = [str(v) for v in value]
        else:
            selected = [str(value)]
        w["selected_json"] = json.dumps(selected, ensure_ascii=False)

        return context


class AccentSelect(_AccentSelectMixin, forms.Select):
    pass


class AccentSelectMultiple(_AccentSelectMixin, forms.SelectMultiple):
    pass
