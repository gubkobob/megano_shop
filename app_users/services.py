"""
Сервисы для работы с пользователями
"""
from django.contrib.auth import get_user_model

User = get_user_model()


def get_10_digits_from_phone_number(phone_number_16_digits: str) -> str:
    """
    Функция берет номер телефона из формы вида +7(999)888-77-66
    и возвращает только 10 цифр 9998887766
    """
    phone_number_10_digits = (
        phone_number_16_digits[3:6]
        + phone_number_16_digits[7:10]
        + phone_number_16_digits[11:13]
        + phone_number_16_digits[14:]
    )
    return phone_number_10_digits


def reset_phone_format(user: User):
    """
    Функция берет номер телефона из БД пользователя +7(999)888-77-66
    и меняет его на 10 цифр 9998887766
    """
    phone_number_16_digits = user.phone_number
    phone_number_10_digits = get_10_digits_from_phone_number(phone_number_16_digits)
    user.phone_number = phone_number_10_digits


class UserServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с пользователями
    """
