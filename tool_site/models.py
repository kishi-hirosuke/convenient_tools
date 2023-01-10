
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import datetime

class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None, created_at=None, updated_at=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name = name,
            email=self.normalize_email(email),
            created_at = created_at,
            updated_at = updated_at,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class AutoBizAccount(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=256)
    token = models.IntegerField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def active(self):
        return self.is_active

    @property
    def staff(self):
        return self.is_staff

    @property
    def admin(self):
        return self.is_admin

    # @property
    # def is_superuser(self):
    #     return self.is_superuser

    class Meta:
        db_table = 'auto_biz_account'


class TimeUser(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=256)
    token = models.IntegerField(unique=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'time_user'
