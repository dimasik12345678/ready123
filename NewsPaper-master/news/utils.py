from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper import settings


def send_notifications(preview, pk, title, subscribers):
    for subscriber in subscribers:
        html_content = render_to_string(
            'post_created_email.html',
            {
                'username': subscriber.username,
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}',
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email]
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()
