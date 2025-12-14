from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def upgrade_me(request):
    """Добавляет авторизованного пользователя в группу 'authors'."""
    user = request.user

    # 1. Проверяем, что пользователь НЕ находится в группе 'authors'.
    # Это предотвращает повторное добавление и лишние запросы к БД.
    if not user.groups.filter(name='Authors').exists():
        # 2. Получаем объект группы 'authors' (если она не найдена, будет ошибка DoesNotExist)
        try:
            author_group = Group.objects.get(name='Authors')
        except Group.DoesNotExist:
            print("Ошибка: Группа 'Authors' не найдена в базе данных!")
            return redirect('/')
        # 3. Добавляем пользователя в группу.
        author_group.user_set.add(user)
    # 4. Перенаправляем пользователя на главную страницу
    return redirect('/')

