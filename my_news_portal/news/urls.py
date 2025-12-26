from django.urls import path
from .views import (
    PostList, PostDetail, PostSearch, PostCreate,
    PostUpdate, PostDelete, ArticleCreate,
    CategoryListView, subscribe
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    # 1. СПИСКИ И ПОИСК
    # Главная страница - кэш на 1 минуту (60 секунд)
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('search/', PostSearch.as_view(), name='post_search'),

    # 2. CRUD: СОЗДАНИЕ
    path('create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),

    # 3. ДЕТАЛЬНАЯ СТРАНИЦА
    # Отдельная новость/статья - кэш на 5 минут (300 секунд)
    path('<int:pk>/', cache_page(60*60*24)(PostDetail.as_view()), name='post_detail'),

    # 4. РЕДАКТИРОВАНИЕ/УДАЛЕНИЕ
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),

    # 5. Категории
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]