from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Author
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post



@receiver(m2m_changed, sender=Post.category.through)
def notify_about_new_post(sender, instance, action, **kwargs):
    # Нас интересует только момент после добавления категорий
    if action == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        # Собираем почты всех подписчиков этих категорий
        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        # Убираем дубликаты (если человек подписан на две категории сразу)
        subscribers_emails = set(subscribers_emails)

        for email in subscribers_emails:
            if not email:
                continue

            # Генерируем HTML из шаблона
            html_content = render_to_string(
                'account/email/new_post_notification.html',
                {
                    'post': instance,
                    'link': f'http://127.0.0.1:8000/news/{instance.id}'
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'✨ У нас кое-что новенькое в разделе {instance.category.first()}!',
                body=instance.text[:50],
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
