from faker import Faker
from phonenumbers import (parse as parse_pn, format_number,
                            is_valid_number, PhoneNumberFormat)

from .models import Contact


Faker.seed(0)
fake = Faker(['fa_IR', 'en_US'])

def insert_fake(count=100):
	added = 0
	while added < count:
		name = fake['en_US'].name()
		numb = fake['fa_IR'].phone_number()
		try:
			numb=parse_pn(numb)
			if not is_valid_number(numb):
				raise Exception()
		except:
			continue
		numb = format_number(numb, PhoneNumberFormat.E164)
		desc = fake['en_US'].text(max_nb_chars=120)
		try:
			Contact(name=name,phone_number=numb,description=desc).save()
			added += 1
		except:
			continue
