from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model

CONDITIONS = [
    ('new', 'New'),
    ('used_good', 'Used - Good Condition'),
    ('used_fair', 'Used - Fair Condition'),
    ('old', 'Old'),
]


class UserManager(BaseUserManager):

    def create_user(self, concordia_id, password=None, **extra_fields):

        if not concordia_id:
            raise ValueError('The Concordia ID is mandatory.')
        user = self.model(concordia_id=concordia_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, concordia_id, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(concordia_id, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):

    concordia_id = models.CharField(max_length=20, unique=True, help_text="Concordia University ID")
    username = None
    USERNAME_FIELD = 'concordia_id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='user_groups',  # Custom related_name
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_user_permissions',  # Custom related_name
        related_query_name='user',
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.concordia_id})"


class Textbook(models.Model):

    title = models.CharField(max_length=255, help_text="Title of the textbook")
    author = models.CharField(max_length=255, help_text="Author(s) of the textbook")
    edition = models.CharField(max_length=50, blank=True, null=True, help_text="Edition of the textbook (optional)")
    condition = models.CharField(max_length=20, choices=CONDITIONS, help_text="Condition of the textbook")
    course_code = models.CharField(max_length=255, help_text="code of the course")
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="owned_textbooks",
                              help_text="Student who owns this textbook")
    is_available = models.BooleanField(default=True, help_text="Whether the textbook is available for trade")

    def __str__(self):
        return f"{self.title} ({self.author})"
