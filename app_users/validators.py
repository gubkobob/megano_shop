from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from app_users.services import get_10_digits_from_phone_number

phone_validator = RegexValidator(
    r"^\+\d\(\d{3}\)\d{3}\-\d{2}\-\d{2}$",
    "Телефон должен быть в формате +7(999)888-77-66",
)


def same_phone_validate(phone_number):
    User = get_user_model()
    phone_number_10_digits = get_10_digits_from_phone_number(phone_number)
    users = User.objects.all()
    for user in users:
        if phone_number_10_digits == user.phone_number:
            msg = "This phone number already used"
            raise ValidationError(msg)


def file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')