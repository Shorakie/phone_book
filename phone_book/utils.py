from faker import Faker
from phonenumbers import (parse as parse_pn, format_number,
                            is_valid_number, PhoneNumberFormat)
import colorful as cf

from .models import Contact


Faker.seed(0)
fake = Faker(['fa_IR', 'en_US'])

def insert_fake(count=100):
    added = 0
    fails = 0
    while added < count and fails < 20:
        first_name = fake['en_US'].first_name()
        last_name = fake['en_US'].last_name()

        number = fake['fa_IR'].phone_number()
        try:
            number=parse_pn(number)
            if not is_valid_number(number):
                raise Exception()
        except:
            continue
        number = format_number(number, PhoneNumberFormat.E164)

        email = fake['fa_IR'].ascii_safe_email()
        desc = fake['en_US'].text(max_nb_chars=120)

        try:
            Contact(first_name=first_name, last_name=last_name, phone_number=number, email=email, description=desc).save()
            added += 1
            fails = 0
        except:
            fails += 1
            continue

    if fails:
        print(cf.orange & cf.bold | 'There was an error with faking contacts!')

