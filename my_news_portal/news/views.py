from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from pyexpat.errors import messages
from unicodedata import category

from .models import Post, ARTICLE, NEWS, Category  # <-- Только Post и константы
from .forms import PostForm
from .filters import PostFilter
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings




# --- 1. Создание НОВОСТЕЙ (URL: /news/create/) ---
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        # Если мы хотим что-то добавить посту перед сохранением (например, тип)
        if self.request.path == '/create/':  # Пример логики для выбора типа
            post.post_type = 'NW'

            # Просто сохраняем объект, Django сам вызовет сигналы
        # и сохранит категории после этого.
        return super().form_valid(form)
# --- 2. Создание СТАТЕЙ (URL: /articles/create/) ---
class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',) # Исправил опечатку news.add.post на news.add_post
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = ARTICLE
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
class PostUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    success_url = reverse_lazy('post_list')


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')
class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        # Получаем категорию из URL
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        # Фильтруем посты по этой категории
        return Post.objects.filter(category=self.category).order_by('-time_in')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем саму категорию в контекст, чтобы отобразить её имя в шаблоне
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})


def send_notifications(post):
    """Универсальная функция для рассылки уведомлений подписчикам"""
    # 1. Находим всех подписчиков для всех категорий этого поста
    subscribers = set()
    for cat in post.category.all():
        subscribers.update(cat.subscribers.all())

    for subscriber in subscribers:
        # Пропускаем, если у пользователя нет почты
        if not subscriber.email:
            continue

        html_content = render_to_string(
            'news/post_created_email.html',
            {
                'post': post,
                'user': subscriber,
            }
        )

        msg = EmailMultiAlternatives(
            subject=post.title,  # Заголовок в теме письма
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()