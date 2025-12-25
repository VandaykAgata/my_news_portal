from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_notifications_task(preview, pk, title,subscribers):
    for sub_email in subscribers:
        html_content = render_to_string(
            'account/email/new_post_notification.html',
            {
                'text': preview,
                'link':f'{settings.SITE_URL}/news/{pk}'
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
@shared_task
def weekly_newsletter_task():
    print("Запущена еженедельная рассылка через Celery!")
