from django_filters import FilterSet, DateFilter, CharFilter
from django import forms
from .models import Post


class PostFilter(FilterSet):
    # 1. ЯВНО ПРОПИСЫВАЕМ ФИЛЬТР ПО НАЗВАНИЮ (без учета регистра,т.к изначально это стало проблемой при поиске)
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',  # <-- Используем icontains для игнорирования регистра
        label='Название содержит'
    )

    # 2. Поиск по имени автора
    author_name = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Поиск по имени автора'
    )

    # 3. Поиск по дате (позже указываемой даты)
    date_after = DateFilter(
        field_name='time_in',
        lookup_expr='date__gte',
        label='Опубликовано после даты',
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Post
        fields = []  # <--- Оставляем пустым, т.к. все поля заданы явно