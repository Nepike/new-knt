from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "authors", "year", "approved", "uploader")
    list_filter = ("approved",)
    search_fields = ("title", "authors")
    autocomplete_fields = ("uploader",)
    filter_horizontal = ("subjects", "terms")
