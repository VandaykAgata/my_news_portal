from django import forms
from django.utils import timezone
from  .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Исключаем поле post_type, потому что мы заполним его сами
        fields = [
            'author',
            'title',
            'text',
            'category',
        ]
    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get('author')
        #Считаем посты за 24 часа
        yesterday = timezone.now() - timezone.timedelta(days=1)
        post_count = Post.objects.filter(author=author, time_in__gt=yesterday).count()
        if post_count >= 3:
            raise  forms.ValidationError("На сегодня хватит, вы опубликовали уже целых 3 новости 😊 Стоит немного отдохнуть, а завтра вернуться с новыми силами ✨")
        return cleaned_data