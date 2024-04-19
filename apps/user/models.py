from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), password=password, username=username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username_validator = RegexValidator(
        r"^[a-zA-Z0-9_]*$", "Only alphanumeric characters are allowed."
    )
    phone_number_validator = RegexValidator(
        r"^(?:\+45|\(\+45\)|\(0045\)|0045|(?!00))\d{8}$", "not valid phone number."
    )
    password_validator = RegexValidator(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$",
        "not valid pass word.",
    )

    username = models.CharField(
        unique=True, max_length=48, validators=[username_validator]
    )
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_operator = models.BooleanField(default=False)
    phone_number = models.CharField(
        unique=True, max_length=11, validators=[phone_number_validator]
    )
    objects = MyUserManager()
    password = models.CharField(max_length=16, validators=[password_validator])

    def __str__(self):
        return self.username


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
