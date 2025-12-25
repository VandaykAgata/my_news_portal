from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms
from news.models import Author


class CommonSignupForm(SignupForm):
    is_author = forms.BooleanField(label='Стать автором', required=False)

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)

        # Если галочка нажата — создаем автора прямо здесь
        if self.cleaned_data.get('is_author'):
            Author.objects.get_or_create(user=user)
            print(f"✅ Автор {user.username} успешно создан через форму!")

        return user