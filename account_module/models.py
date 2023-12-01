from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager
import pyotp


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(
        max_length=300,
        db_column='recovery_email',
        verbose_name='recovery email',
        db_index=True,
        null=True,
        blank=True,
        unique=True
    )
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True, unique=True, db_index=True,
                                    verbose_name='phone number')
    profile_photo = models.ImageField(upload_to='profile_photos', null=True, blank=True, verbose_name='profile photo')

    REQUIRED_FIELDS = ['email', 'phone_number']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username


class Signature(models.Model):
    signature = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bold = models.BooleanField(default=False)
    italic = models.BooleanField(default=False)
    color_choices = [
        ('g', 'green'),
        ('b', 'blue'),
        ('r', 'red'),
        ('p', 'purple')
    ]
    color = models.CharField(max_length=1, choices=color_choices, null=True, blank=True)

    class Meta:
        verbose_name = 'signature'
        verbose_name_plural = 'signatures'

    def __str__(self):
        return self.signature


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100, verbose_name='contact saved name', null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.contact


class OtpCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def generate_code(self):
        totp = pyotp.TOTP(pyotp.random_base32(), digits=6)
        self.code = totp.now()

    def __str__(self):
        return self.code


class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='previous_passwords')
    password = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.password








