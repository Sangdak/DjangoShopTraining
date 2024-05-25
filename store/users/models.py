from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


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
        send_mail(
            'Mail Subject',
            'Mail Message',
            'Email From Address',
            [self.user.email],
            fail_silently=False,
        )
