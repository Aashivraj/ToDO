from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    team_department = models.CharField(max_length=100)

    def __str__(self):
        return self.team_department

class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, email, mobile_number, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not user_name:
            raise ValueError('The User Name field must be set')
        if not mobile_number:
            raise ValueError('The Mobile Number field must be set')
        if role is None:
            raise ValueError('The Role field must be set')

        email = self.normalize_email(email)
        user = self.model(
            user_name=user_name,
            email=email,
            mobile_number=mobile_number,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, mobile_number, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_name, email, mobile_number, role, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER = (
        ('1', 'Admin'),
        ('2', 'TeamLeader'),
        ('3', 'Developer'),
    )

    user_name = models.CharField(_("user name"), max_length=150, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    mobile_number = models.CharField(_("mobile number"), max_length=15, unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    role = models.CharField(max_length=50, choices=USER, default='3')
    photo = models.ImageField(_("photo"), upload_to="user_photos/", blank=True, null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = ["email", "mobile_number", "role"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def toggle_active_status(self):
        self.is_active = not self.is_active
        self.save()
    def get_full_name(self):
        """Return the full name of the user."""
        return self.user_name

    def get_short_name(self):
        """Return the short name of the user."""
        return self.user_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    

class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    updated_by=models.CharField(max_length=20,blank=True, null=True)
 



    def __str__(self):
        return self.title


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_notifications', on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification from {self.sender} to {self.receiver} about {self.todo}'

    @property
    def display_message(self):
        return f"{self.message} ✓✓" if self.is_read else self.message

class Notes(models.Model):
    todo = models.ForeignKey(Todo, related_name='notes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    updated_by=models.CharField(max_length=20,blank=True, null=True)
    
    def __str__(self):
        return self.description



class SystemSettings(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50)
    company_logo = models.TextField()
    location=models.CharField(max_length=200)
    company_info=models.TextField()
    small_logo = models.TextField(blank=True, null=True)  # New field for small logo
    mobile = models.CharField(_("mobile number"), max_length=15, unique=True)
    email = models.CharField(max_length=30)
    facebook = models.CharField(max_length=70)
    instagram = models.CharField(max_length=70)
    linkdein = models.CharField(max_length=70)
    company_link = models.CharField(max_length=70)
    