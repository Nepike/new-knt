from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone


def file_upload_to(instance, filename):
    if instance.material_id:
        return f"materials/{instance.material_id}/files/{filename}"
    if instance.book_id:
        return f"books/{instance.book_id}/files/{filename}"
    return f"files/{filename}"


def image_upload_to(instance, filename):
    if instance.material_id:
        return f"materials/{instance.material_id}/images/{filename}"
    return f"images/{filename}"


def human_size(num_bytes):
    if num_bytes is None:
        return ""
    size = float(num_bytes)
    for unit in ("Б", "КБ", "МБ", "ГБ", "ТБ"):
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "Б" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} ПБ"


class File(models.Model):
    material = models.ForeignKey("materials.Material", verbose_name="материал", on_delete=models.CASCADE, related_name="files", null=True, blank=True)
    book = models.ForeignKey("library.Book", verbose_name="книга", on_delete=models.CASCADE, related_name="files", null=True, blank=True)

    name = models.CharField("название", max_length=150)
    # TODO (M2): file -> Cloudflare R2 (django-storages), пока локально
    file = models.FileField("файл", upload_to=file_upload_to)
    size = models.PositiveBigIntegerField("размер (байт)", null=True, blank=True)
    downloads = models.PositiveIntegerField("скачиваний", default=0)
    order = models.PositiveIntegerField("порядок", default=0)

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="загрузил", on_delete=models.SET_NULL, null=True, blank=True, related_name="uploaded_files")
    created = models.DateTimeField("создан", default=timezone.now)

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "файлы"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    def clean(self):
        if not self.material and not self.book:
            raise ValidationError("Файл должен быть привязан к материалу или книге.")
        if self.material and self.book:
            raise ValidationError("Файл не может быть привязан и к материалу, и к книге одновременно.")

    def save(self, *args, **kwargs):
        if self.file and not self.size:
            self.size = self.file.size
        super().save(*args, **kwargs)

    def human_size(self):
        return human_size(self.size)


class Image(models.Model):
    material = models.ForeignKey("materials.Material", verbose_name="материал", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    # TODO (shop): product FK на shop.Product (картинка товара) — добавить при создании shop

    name = models.CharField("название", max_length=150, blank=True)
    # TODO (M2): image -> Cloudflare R2 (django-storages), пока локально
    image = models.ImageField("изображение", upload_to=image_upload_to)
    size = models.PositiveBigIntegerField("размер (байт)", null=True, blank=True)
    order = models.PositiveIntegerField("порядок", default=0)

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="загрузил", on_delete=models.SET_NULL, null=True, blank=True, related_name="uploaded_images")
    created = models.DateTimeField("создан", default=timezone.now)

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name or f"изображение #{self.pk}"

    def save(self, *args, **kwargs):
        if self.image and not self.size:
            self.size = self.image.size
        super().save(*args, **kwargs)

    def human_size(self):
        return human_size(self.size)


# Удаляем сам файл из хранилища при удалении записи (иначе остаётся «сирота»).
# Работает и для локального диска, и для R2 — storage.delete() одинаков.
@receiver(post_delete, sender=File)
def delete_file_blob(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)


@receiver(post_delete, sender=Image)
def delete_image_blob(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
