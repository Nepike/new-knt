from django import forms

from .widgets import AccentSelect, AccentSelectMultiple

SUBJECTS = [
    ("1", "Алгебра"), ("2", "Геометрия"), ("3", "Математический анализ"),
    ("4", "Физика"), ("5", "Программирование"), ("6", "Английский язык"),
]
TEACHERS = [
    ("1", "Петров А.С."), ("2", "Сидорова Е.В."), ("3", "Иванов И.И."),
    ("4", "Кузнецова О.П."), ("5", "Смирнов Д.А."),
]
PLANS = [("free", "Бесплатно"), ("pro", "Про"), ("team", "Командный")]


class DemoForm(forms.Form):
    subject_plain = forms.ChoiceField(choices=SUBJECTS, required=False, widget=AccentSelect(label="Предмет"))
    subject_search = forms.ChoiceField(choices=SUBJECTS, required=False, widget=AccentSelect(search=True, label="Предмет"))
    teachers_plain = forms.MultipleChoiceField(choices=TEACHERS, required=False, widget=AccentSelectMultiple(label="Преподаватели"))
    teachers_search = forms.MultipleChoiceField(choices=TEACHERS, required=False, widget=AccentSelectMultiple(search=True, label="Преподаватели"))

    # Текстовые поля: placeholder=" " нужен для плавающего лейбла (:placeholder-shown).
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "input peer", "placeholder": " "}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "input peer", "placeholder": " "}))
    count = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "input peer", "placeholder": " "}))
    event_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": "input peer", "type": "date"}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "textarea peer", "placeholder": " ", "rows": 3}))

    plan = forms.ChoiceField(choices=PLANS, required=False, widget=forms.RadioSelect(attrs={"class": "accent-accent"}))
    anon = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "w-5 h-5 rounded accent-accent"}))
    notify = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "peer sr-only"}))
