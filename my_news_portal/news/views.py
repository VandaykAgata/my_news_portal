from django.shortcuts import render
from .models import Post, Comment  # <-- Добавь импорт Comment


def PostList(request):
    posts = Post.objects.all()

    # --- ВРЕМЕННОЕ ПОЛУЧЕНИЕ КОММЕНТАРИЕВ ДЛЯ ПРИМЕРА ---
    # Мы получим все комментарии, чтобы потом передать их в HTML
    comments = Comment.objects.all()
    # -----------------------------------------------------

    context = {
        'posts': posts,

    }

    return render(request, 'news/post_list.html', context)