from .models import Category, Post
from modeltranslation.translator import register, TranslationOptions

# Перевод для категорий
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',) # Поле названия категории

# Перевод для постов (новостей/статей)
@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text',) # Заголовок и содержание