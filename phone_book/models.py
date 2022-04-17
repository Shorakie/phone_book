from peewee import Model, CharField, TextField
import colorful as cf

from .settings import db


class Contact(Model):
    first_name = CharField(max_length=64, index=True)
    last_name = CharField(max_length=64, null=True, index=True)
    phone_number = CharField(max_length=14, index=True, unique=True)
    email = CharField(max_length=320, null=True)
    description = TextField(null=True)
    
    @property
    def name(self):
        return ' '.join([name for name in [self.first_name, self.last_name] if name])

    def __str__(self):
        string = f"Name 🧑: {cf.deepSkyBlue & cf.bold | self.name}\nPhone number 📱: {cf.deepSkyBlue & cf.bold | self.phone_number}"
        if self.email:
            string += f"\nEmail 📧: {cf.skyBlue & cf.bold | self.email}"
        if self.description:
            string += f"\nDescription 📃: {cf.skyBlue & cf.bold | self.description}"
        return string

    class Meta:
        database = db

