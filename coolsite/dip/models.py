from django.db import models
from django.urls import reverse


class Lecture(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content_lecture = models.FileField(upload_to='uploads_Lecture/%Y/%m/%d/', verbose_name="Файлы лекций")
    content_laboratory = models.FileField(upload_to='uploads_Laboratory/%Y/%m/%d/', null=True, verbose_name="Файлы лабораторных работ")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликован\\Неопубликован")

    def __str__(self):
        return self.title

    def get_absolute_url_lecture(self):
        return reverse('lecture', kwargs={'lecture_slug': self.slug})

    def get_absolute_url_laboratory(self):
        return reverse('laboratory', kwargs={'laboratory_slug': self.slug})

    class Meta:
        verbose_name = "Лекции"
        verbose_name_plural = "Лекции"
        ordering = ['time_create', 'title']
