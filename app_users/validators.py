from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    r"^\+\d\(\d{3}\)\d{3}\-\d{2}\-\d{2}$",
    "Телефон должен быть в формате +7(999)888-77-66",
)


def email_exist_validator(email: str):
    """
    Функция валидации - проверка почты на существование в БД сайта
    """
    User = get_user_model()
    users = User.objects.all()
    flag = False
    for user in users:
        if user.email == email:
            flag = True
    if not flag:
        msg = "No user with this email on site"
        raise ValidationError(msg)


def file_size(value):
    """
    Функция валидации - проверка картинки на обьем менее 2МБ
    """
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 2 MiB.")
