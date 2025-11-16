from django.urls import path

#from .models import Article
from .views import ArticleDetailView,ArticleListView


urlpatterns = [
    # Пустая строка '' означает, что это корневой адрес внутри news/.
    # Полный путь: http://127.0.0.1:8000/news/
    path('',ArticleListView.as_view(), name='article_list'),
    path('<int:pk>', ArticleDetailView.as_view(), name='article_detail'),


]
