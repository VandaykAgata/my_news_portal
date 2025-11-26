from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Post, ARTICLE, NEWS  # <-- Только Post и константы
from .forms import PostForm
from .filters import PostFilter


# --- 1. Создание НОВОСТЕЙ (URL: /news/create/) ---
class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = NEWS  # <-- Устанавливаем тип "Новость"
        return super().form_valid(form)


# --- 2. Создание СТАТЕЙ (URL: /articles/create/) ---
class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = ARTICLE  # <-- Устанавливаем тип "Статья"
        return super().form_valid(form)


# --- 3. ГЛАВНАЯ СТРАНИЦА (URL: /news/) ---
class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Перехватываем, чтобы показывать ТОЛЬКО НОВОСТИ (как требует задание)
    def get_queryset(self):
        # Filter: Показываем только объекты с post_type='NW'
        return Post.objects.filter(post_type=NEWS).order_by(self.ordering)


# --- 4. СТРАНИЦА ПОИСКА (URL: /news/search/) ---
class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news/post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Используем PostFilter для фильтрации по всем критериям
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# --- 5. ДЕТАЛЬНАЯ СТРАНИЦА (Общая для новостей и статей) ---
class PostDetail(DetailView):
    model = Post
    template_name = 'news/post_detail.html'  # Предполагается, что этот шаблон существует
    context_object_name = 'post'


# --- 6. РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ ---
class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    success_url = reverse_lazy('post_list')


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')