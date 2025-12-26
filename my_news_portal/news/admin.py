from django.contrib import admin
from .models import Post, Category, PostCategory

# Это позволит добавлять категории прямо внутри статьи
class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1 # Сколько пустых строк для выбора категорий показать сразу

class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInline]

# Регистрируем модели
admin.site.register(Post, PostAdmin)
admin.site.register(Category)