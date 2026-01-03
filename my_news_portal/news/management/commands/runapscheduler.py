import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from news.models import Post, Category

logger = logging.getLogger(__name__)


def my_job():
    today = timezone.now()
    last_week = today - timedelta(days=7)

    # Исправила поле на time_in, как в твоем tasks.py
    posts = Post.objects.filter(time_in__gte=last_week)

    if not posts.exists():
        return

    # Получаем все категории, в которых были посты за неделю
    categories = posts.values_list('category', flat=True).distinct()

    # Собираем всех подписчиков этих категорий
    subscribers_emails = set(
        Category.objects.filter(id__in=categories)
        .values_list('subscribers__email', flat=True)
    )

    for email in subscribers_emails:
        if not email:
            continue

        # Посты именно тех категорий, на которые подписан этот конкретный email
        user_posts = posts.filter(category__subscribers__email=email).distinct()

        html_content = render_to_string(
            'news/daily_post.html',  # Путь как в твоем tasks.py
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


# Дальше идет стандартный код запуска (class Command), который я давала выше
class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger="cron",
            day_of_week="mon",  # Раз в неделю по понедельникам
            hour="00",
            minute="00",
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()