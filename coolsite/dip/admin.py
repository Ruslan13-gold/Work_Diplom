from django.contrib import admin

from .models import *


class CursAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content_lecture', 'content_laboratory', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Lecture, CursAdmin)
