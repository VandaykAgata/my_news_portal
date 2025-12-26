from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import send_notifications_task
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    # Убираем проверку на post_add, чтобы ловить ЛЮБОЕ добавление категории
    action = kwargs.get('action')

    # Добавляем принты — они появятся в окне, где запущен runserver
    print(f"DEBUG: Сигнал сработал! Действие: {action}")

    if action == 'post_add':
        # Получаем список email
        subscribers = instance.category.all().values_list('subscribers__email', flat=True).distinct()

        print(f"DEBUG: Найдено подписчиков: {len(subscribers)}")

        if subscribers:
            send_notifications_task.delay(
                instance.preview(),
                instance.pk,
                instance.title,
                list(subscribers)
            )
            print("DEBUG: Задача отправлена в Celery!")

@receiver(post_save, sender=User)
def welcome_email(sender, instance, created, **kwargs):
    if created:  # Если пользователь только что создан
        send_mail(
            subject=f'Привет, {instance.username}!',
            message='Добро пожаловать в наш новостной портал! Теперь вы можете подписываться на любимые категории.',
            from_email= settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
        )