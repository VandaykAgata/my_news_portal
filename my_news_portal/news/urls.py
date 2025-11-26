from django.urls import path
from .views import (
    PostList,  # <-- Для корневой страницы (список новостей)
    PostSearch,
    PostCreate,
    ArticleCreate,
    PostUpdate,
    PostDelete
)


urlpatterns = [
    # 1. СПИСКИ И ПОИСК
    path('', PostList.as_view(), name='post_list'),
    path('search/', PostSearch.as_view(), name='post_search'),

    # 2. CRUD: СОЗДАНИЕ (разделяем по типу поста)
    path('create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),

    # 4. CRUD: РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ НОВОСТЕЙ
    # Добавлен префикс 'news/'
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

    # 5. CRUD: РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ СТАТЕЙ
    # Добавлен префикс 'articles/'
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]