from django import forms


class _AccentSelectMixin:
    """Метка наших селектов: несёт флаг поиска. Разметку рисует core/inputs.html (фильтр select_json)."""

    def __init__(self, *args, search=False, **kwargs):
        self.search = search
        super().__init__(*args, **kwargs)


class AccentSelect(_AccentSelectMixin, forms.Select):
    pass


class AccentSelectMultiple(_AccentSelectMixin, forms.SelectMultiple):
    pass
