from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import send_notifications_task


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        # Выбираем все email подписчиков для всех категорий этой новости разом
        subscribers = instance.category.all().values_list('subscribers__email', flat=True).distinct()

        # Передаем список в задачу Celery
        # Мы используем list(subscribers), так как Celery любит простые списки
        send_notifications_task.delay(
            instance.preview(),
            instance.pk,
            instance.title,
            list(subscribers)
        )