from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


# 1. Создаем "вставку" для категорий
class CategoryInline(admin.TabularInline):
    model = PostCategory  # Используем твою таблицу-посредник
    extra = 1  # Сколько пустых строк для выбора категорий показать сразу


# 2. Настройка для Постов
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_type', 'time_in', 'rating', 'get_categories')
    list_filter = ('post_type', 'author', 'time_in')
    search_fields = ('title', 'author__user__username')

    # Вставляем выбор категорий прямо в страницу поста
    inlines = [CategoryInline]

    # Функция для показа категорий в списке
    def get_categories(self, obj):
        # Берем все категории, связанные с этим постом
        return ", ".join([c.name for c in obj.category.all()])

    get_categories.short_description = 'Категории'


# 3. Регистрация остальных моделей
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)