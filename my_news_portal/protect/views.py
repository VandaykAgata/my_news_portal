from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверяем, ЕСТЬ ЛИ пользователь в группе 'authors'
        # exists() возвращает True/False, это очень эффективно.

        is_author = self.request.user.groups.filter(name='author').exists()

        # Передаем в шаблон, НЕ является ли он автором (для показа кнопки)
        context['is_not_author'] = not is_author
        return context




