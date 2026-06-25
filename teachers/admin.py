from django.contrib import admin

from .models import Review, Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("surname", "name", "patronymic")
    search_fields = ("surname", "name")
    filter_horizontal = ("subjects",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("teacher", "author", "created")
    search_fields = ("teacher__surname", "author__email")
    autocomplete_fields = ("teacher", "author")
