from django.contrib import admin
from .models import Post, Category, Author

admin.site.register(Post)
admin.site.register(Category)


class AuthorAdmin(admin.ModelAdmin):
    # Используем имена из модели (user и rating)
    list_display = ('id', 'user', 'rating')

    # Чтобы поиск работал, обращаемся к полю username внутри модели User
    search_fields = ('user__username',)


# Регистрируем модель Author с нашими новыми настройками
admin.site.register(Author, AuthorAdmin)