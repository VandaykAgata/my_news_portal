from django.urls import path
from .views import PostList # Импортируем нашу будущую функцию

urlpatterns = [
    # Пустая строка '' означает, что это корневой адрес внутри news/.
    # Полный путь: http://127.0.0.1:8000/news/
    path('', PostList, name='post_list'),
]