import re

from prompt_toolkit.validation import ValidationError, Validator as _Validator
from phonenumbers import parse as parse_phone_number, is_valid_number 


class Validator(_Validator):
    def __and__(self, other):
        return AndValidator(self, other)


class AndValidator(Validator):
    def __init__(self, rhs, lhs):
        self._rhs = rhs
        self._lhs = lhs

    def validate(self, document) -> None:
        self._rhs.validate(document)
        self._lhs.validate(document)


class RegexValidator(Validator):
    def __init__(
        self,
        regex: str,
        message: str="Input is not valid",
    ) -> None:
        self._message = message
        self._re = re.compile(regex)

    def validate(self, document) -> None:
        if not self._re.match(document.text):
            raise ValidationError(
                message=self._message, cursor_position=document.cursor_position
            )


class PhoneNumberValidator(Validator):
    def __init__(
        self,
        message: str="Input is not a valid phone number",
    ) -> None:
        self._message = message

    def validate(self, document) -> None:
        try:
            if not is_valid_number(parse_phone_number(document.text, 'IR')):
                raise Exception()
        except:
            raise ValidationError(
                message=self._message, cursor_position=document.cursor_position
            )


class UniqueValidator(Validator):
    def __init__(
        self,
        clazz,
        field,
        message: str="Input is not unique"
    ):
        self._clazz = clazz
        self._field = field
        self._message = message

    def validate(self, document) -> None:
        if self._clazz.select().where(self._field == document.text).exists():
            raise ValidationError(
                message=self._message, cursor_position=document.cursor_position
            )

