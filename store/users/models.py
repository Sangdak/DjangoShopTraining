from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification (models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object fot {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'code': self.code, 'email': self.user.email})
        host = settings.ALLOWED_HOSTS[0]
        verification_link = f'http://{"localhost:8000" if host == "localhost" else host}{link}'
        mail_subject = f'Подтверждение учётной записи для {self.user.username}'
        mail_message = f'Для подтверждения учётной записи {self.user.username} перейдите по ссылке: {verification_link}'
        html_message = (f'Для подтверждения учётной записи {self.user.username} '
                        f'перейдите по <a href="{verification_link}">ссылке</a>')
        send_mail(
            mail_subject,
            mail_message,
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,
            html_message=html_message,
        )

    def is_expired(self):
        return now() >= self.expiration
