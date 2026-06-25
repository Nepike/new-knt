from django.contrib import admin

from .models import File, Image


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("name", "material", "book", "downloads", "order")
    search_fields = ("name",)
    autocomplete_fields = ("material", "book", "uploader")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("name", "material", "order")
    search_fields = ("name",)
    autocomplete_fields = ("material", "uploader")
