from django.contrib import admin
from .models import Category, Post
from modeltranslation.admin import TranslationAdmin
# импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

# Register your models here.

class CategoryAdmin(TranslationAdmin):
    model = Category

class PostAdmin(TranslationAdmin):
    model = Post

admin.site.register(Category)
admin.site.register(Post)