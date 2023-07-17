from .models import Order

"""
Сервисы для работы с заказами
"""


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


def reset_phone_format(order: Order):
    """
    Функция берет номер телефона из БД пользователя +7(999)888-77-66
    и меняет его на 10 цифр 9998887766
    """
    phone_number_16_digits = order.phone_number
    phone_number_10_digits = get_10_digits_from_phone_number(phone_number_16_digits)
    order.phone_number = phone_number_10_digits
