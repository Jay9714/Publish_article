from django.contrib import admin
from .models import Article,Tag
# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["status", "img", "content", "title", "user"][::-1]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]
