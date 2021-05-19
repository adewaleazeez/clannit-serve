from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def test_send():
    subject = 'EMAIL SUBMISSION SUCCESSFUL'
    message = 'WELCOME TO {}'.format(settings.SITE_URL)
    html_message = loader.render_to_string(
        'site/user/email.html',
        {
            'link': '{}?refCode={}'.format(settings.SITE_URL,327263)
        }
    )
    send_mail(subject, message, ('WORKSFAIR TEAM ' + 'noreply@worksfair.com'), ['infozvil@gmail.com'], fail_silently=True,
              html_message=html_message)


@shared_task
def hello_world():
    hello = "Hello World my people"
    return hello



