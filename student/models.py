from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.core.validators import EmailValidator
# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class StudentClass(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField('email address', unique=True, validators=[EmailValidator(message="Please enter a valid email address.")] )
    first_name = models.CharField('first name', max_length=30, blank=True, null=True )
    last_name = models.CharField('last name', max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='student/images', blank=True, null=True)
    student_class = models.ForeignKey(StudentClass, related_name='user_class', on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email