import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from news.models import Post
from unicodedata import category


class Command(BaseCommand):
    help = 'Отправка еженедельного дайджеста новостей'

    def handle(self, *args, **options):
        # 1. Определяем временной порог (7 дней назад)
        week_ago = timezone.now() - datetime.timedelta(days=7)

        # 2. Берем всех пользователей, у которых есть подписки
        # (category__isnull=False + distinct гарантируют, что возьмем только подписчиков без повторов)
        users = User.objects.filter(categories__isnull=False).distinct()

        for user in users:
            # 3. Собираем все посты из всех категорий пользователя за неделю
            # Мы используем __in, чтобы найти посты сразу во всех категориях юзера
            user_categories = user.categories.all()
            posts = Post.objects.filter(
                category__in=user_categories,
                time_in__gte=week_ago,
            ).distinct()

            if posts.exists():
                # 4. Если новости есть, готовим письмо
                html_content = render_to_string(
                    'weekly_digest_email.html',
                    {'user': user,
                     'posts': posts,
                     'link': 'http://127.0.0.1:8000'
                     }
                )

            msg = EmailMultiAlternatives(
                subject=f'Дайджест новостей за неделю, {user.username}!',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            self.stdout.write(self.style.SUCCESS(f'Письмо отправлено: {user.username}'))

