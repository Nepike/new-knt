from django import forms

from .models import SCORE_LABELS, Review

SCORE_FIELDS = tuple(SCORE_LABELS)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = SCORE_FIELDS + ("text", "hide_author")
        labels = {**SCORE_LABELS, "text": "Текст отзыва", "hide_author": "Оставить анонимно"}
        widgets = {"text": forms.Textarea(attrs={"rows": 4})}

    def score_fields(self):
        return [self[name] for name in SCORE_FIELDS]

    def clean(self):
        data = super().clean()
        if not data.get("text") and not any(data.get(name) for name in SCORE_FIELDS):
            raise forms.ValidationError("Поставь хотя бы одну оценку или напиши текст отзыва.")
        return data
