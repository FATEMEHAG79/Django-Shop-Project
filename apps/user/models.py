from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import slugify

from apps.user.managers import UserManager
from apps.core.models import TimeStampMixin, LogicalMixin
from django.utils.translation import gettext_lazy as _


gender = [("f", "female"), ("m", "mail")]


class User(LogicalMixin, AbstractUser, TimeStampMixin):
    username_validator = RegexValidator(
        "^[a-zA-Z0-9_]*$", "Only alphanumeric characters are allowed."
    )
    username = models.CharField(
        unique=True,
        max_length=48,
        validators=[username_validator],
        error_messages={"unique": ("A user with this username already exists")},
        null=True,blank=True
    )
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=48, choices=gender)
    birthday = models.DateTimeField(null=True, blank=True)
    slug=models.SlugField(max_length=80)
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


class Address(models.Model):
    zip_cod_validator = RegexValidator(
        r"\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b", "not valid zip code."
    )
    IRANIAN_PROVINCES = [
        ("alborz", "البرز"),
        ("ardabil", "اردبیل"),
        ("east_azarbaijan", "آذربایجان شرقی"),
        ("west_azarbaijan", "آذربایجان غربی"),
        ("bushehr", "بوشهر"),
        ("chaharmahal_and_bakhtiari", "چهارمحال و بختیاری"),
        ("fars", "فارس"),
        ("gilan", "گیلان"),
        ("golestan", "گلستان"),
        ("hamadan", "همدان"),
        ("hormozgan", "هرمزگان"),
        ("ilam", "ایلام"),
        ("isfahan", "اصفهان"),
        ("kerman", "کرمان"),
        ("kermanshah", "کرمانشاه"),
        ("khorasan_razavi", "خراسان رضوی"),
        ("khuzestan", "خوزستان"),
        ("kohgiluyeh_and_boyer-ahmad", "کهگیلویه و بویراحمد"),
        ("kordestan", "کردستان"),
        ("lorestan", "لرستان"),
        ("markazi", "مرکزی"),
        ("mazandaran", "مازندران"),
        ("north_khorasan", "خراسان شمالی"),
        ("qazvin", "قزوین"),
        ("qom", "قم"),
        ("semnan", "سمنان"),
        ("sistan_and_baluchestan", "سیستان و بلوچستان"),
        ("south_khorasan", "خراسان جنوبی"),
        ("tehran", "تهران"),
        ("yazd", "یزد"),
        ("zanjan", "زنجان"),
    ]
    province = models.CharField(max_length=50, choices=IRANIAN_PROVINCES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=48, validators=[zip_cod_validator])

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Addresses"
