from datetime import date

from django.db import models


class Subject(models.Model):
    name = models.CharField("название", max_length=50)
    dative = models.CharField("название (дательный падеж)", max_length=50)
    accusative = models.CharField("название (винительный падеж)", max_length=50)

    class Meta:
        verbose_name = "предмет"
        verbose_name_plural = "предметы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Term(models.Model):
    number = models.PositiveSmallIntegerField("номер")

    class Meta:
        verbose_name = "семестр"
        verbose_name_plural = "семестры"
        ordering = ["number"]

    def __str__(self):
        return f"Семестр {self.number}"


class Team(models.Model):
    STAGE_CHOICES = (
        ("bachelor", "Бакалавриат"),
        ("master", "Магистратура"),
    )

    number = models.CharField("номер", max_length=7, unique=True)
    profile = models.CharField("профиль", max_length=255)
    course_code = models.CharField("направление (код курса)", max_length=10)
    stage = models.CharField("ступень обучения", max_length=20, choices=STAGE_CHOICES)
    year_of_admission = models.PositiveSmallIntegerField("год зачисления")

    class Meta:
        verbose_name = "учебная группа"
        verbose_name_plural = "учебные группы"
        ordering = ["number"]

    def __str__(self):
        return self.number

    def get_grade_level(self):
        today = date.today()
        level = today.year - self.year_of_admission
        if today.month >= 9:
            level += 1
        return level + (4 if self.stage == "master" else 0)

    def graduation_year(self):
        return self.year_of_admission + (2 if self.stage == "master" else 6)

    def get_grade_str(self):
        if date.today().year > self.graduation_year():
            return f"Выпускник {self.graduation_year()} года"
        return f"Студент {self.get_grade_level()} курса"
