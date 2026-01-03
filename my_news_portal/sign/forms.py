from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms
from news.models import Author


class CommonSignupForm(SignupForm):
    is_author = forms.BooleanField(label='Стать автором', required=False)

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)

        # Автоматически добавляем КАЖДОГО нового пользователя в группу common
        common_group, _ = Group.objects.get_or_create(name='common')
        user.groups.add(common_group)

        # Если галочка нажата — создаем автора прямо здесь
        if self.cleaned_data.get('is_author'):
            Author.objects.get_or_create(user=user)
            # Добавляем его также в группу авторов, чтобы у него были права на правку
            authors_group, _ = Group.objects.get_or_create(name='authors')
            user.groups.add(authors_group)
            print(f"✅ Автор {user.username} успешно создан через форму!")

        return user