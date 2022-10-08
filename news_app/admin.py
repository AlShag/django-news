from django.contrib import admin
from .models import News, Tag


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "thumbnail",
    )
    search_fields = (
        "title",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
