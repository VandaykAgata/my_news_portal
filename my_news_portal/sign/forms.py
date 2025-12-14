from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class CommonSignupForm(SignupForm):
    """
    Кастомизированная форма регистрации allauth.
    Автоматически добавляет пользователя в группу 'common'.
    """
    def save(self, request):
        # 1. Вызываем родительский метод для сохранения пользователя
        user = super(CommonSignupForm, self).save(request)
        # 2. Получаем группу 'common'
        common_group = Group.objects.get(name='Common')
        # 3. Добавляем пользователя в группу
        common_group.user_set.add(user)
        # 4. Добавляем пользователя в группу
        return user

