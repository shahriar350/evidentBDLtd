from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    def create_user(self, name, phone_number, password, **extra_fields):
        if Users.objects.filter(phone_number=phone_number).count() > 0:
            raise ValidationError(_('Phone number is already taken'))
        if not phone_number:
            raise ValidationError(_('Phone number is required'))
        if len(phone_number) != 11:
            raise ValidationError(_('Phone number must be 11 number'))
        if phone_number[0] != '0' and phone_number[1] != '1':
            raise ValidationError(_('Phone number must be start with 01'))
        if not password:
            raise ValidationError(_('Password is required'))
        if not phone_number.isnumeric():
            raise ValidationError(_('Phone number must be numeric'))
        extra_fields.setdefault("active", True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.last_login = timezone.now()
        user.name = name.title()
        user.save(using=self._db)
        return user

    def create_superuser(self, name, phone_number, password, **extra_fields):
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("admin", True)
        extra_fields.setdefault("active", True)
        user = self.create_user(name, phone_number, password, **extra_fields)
        return user


class Users(AbstractBaseUser):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    name = models.CharField(_('Your name'), max_length=100,
                            validators=[
                                RegexValidator(
                                    regex=r'^[a-zA-Z ]*$',
                                    message=_('name must be Alpha'),
                                ),
                            ]
                            )
    phone_number = models.CharField(_('Phone number'), max_length=11, unique=True)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin
