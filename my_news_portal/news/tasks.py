import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from celery import shared_task
from .models import Post, Category



@shared_task
def weekly_newsletter_task():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)

    if not posts.exists():
        return

    # Собираем уникальные email всех подписчиков, чьи категории обновились
    subscribers_emails = set(
        Category.objects.filter(posts__in=posts)
        .values_list('subscribers__email', flat=True)
    )

    for email in subscribers_emails:
        if not email:
            continue

        # Фильтруем посты специально для этого подписчика
        user_posts = posts.filter(category__subscribers__email=email).distinct()

        html_content = render_to_string(
            'news/daily_post.html',
            {
                'link': settings.SITE_URL,
                'posts': user_posts,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_notifications_task(preview, pk, title, subscribers):
    for sub_email in subscribers:
        html_content = render_to_string(
            'account/email/new_post_notification.html',
            {
                'text': preview,
                'link': f'{settings.SITE_URL}/{pk}'  # Убрала /news/, так как в urls.py у тебя просто <int:pk>/
            }
        )
        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()