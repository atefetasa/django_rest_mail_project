from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    creates a user with given username and password
    and prevents to register a user who didn't provide a phone number or recovery email address
    """
    def create_user(self, username, password, email, phone_number, **extra_fields):
        if (not email) and (not phone_number):
            raise ValueError('one of the email or phone number fields must be set')
        extra_fields.setdefault('is_active', False)
        if email == '':
            email = None
        if phone_number == '':
            phone_number = None
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, email, phone_number, **extra_fields):
        """
        this method creates a superuser with the given username and password
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, email, phone_number, **extra_fields)


