from django import forms
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