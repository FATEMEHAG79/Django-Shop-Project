from django.contrib.auth.models import AbstractUser,Group
from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import slugify
from apps.user.managers import UserManager
from apps.core.models import TimeStampMixin, LogicalMixin
from django.utils.translation import gettext_lazy as _


gender = [("femail", "female"), ("mail", "mail")]


class User(LogicalMixin, AbstractUser, TimeStampMixin):
    username_validator = RegexValidator(
        "^[a-zA-Z0-9_]*$", "Only alphanumeric characters are allowed."
    )
    username = models.CharField(
        unique=True,
        max_length=48,
        validators=[username_validator],
        error_messages={"unique": ("A user with this username already exists")},
        null=True,
        blank=True,
    )
    groups = models.ForeignKey(Group,on_delete=models.CASCADE,blank=True,null=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=48, choices=gender)
    birthday = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    is_active = models.BooleanField(_("active"), default=False)
    phone_number = models.BigIntegerField(
        _("phone_number"),
        unique=True,
        validators=[RegexValidator(r"^989[0-3,9]\d{8}$")],
        error_messages={"unique": ("A user with mobile number already exists")},
        null=True,
    )
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
        ]

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class Address(LogicalMixin, TimeStampMixin):
    province = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=50)
    first_name_recivier= models.CharField(max_length=50)
    last_name_recivier  = models.CharField(max_length=50)
    phone_number_reciver = models.BigIntegerField(
        validators=[RegexValidator(r"^989[0-3,9]\d{8}$")],
        error_messages={"unique": ("A user with mobile number already exists")},
        null=True,blank=True
    )

    def __str__(self):
        return self.user.username


    class Meta:
        verbose_name_plural = "Addresses"


