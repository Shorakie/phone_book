from peewee import Model, CharField, TextField
import colorful as cf

from .settings import db


class Contact(Model):
    name = CharField(max_length=64, index=True)
    phone_number = CharField(max_length=14, index=True, unique=True)
    description = TextField(null=True)

    def __str__(self):
        string = f"Name 🧑: {cf.deepSkyBlue & cf.bold | self.name}\nPhone number 📱: {cf.deepSkyBlue & cf.bold | self.phone_number}"
        if self.description:
            string += f"\nDescription 📃: {cf.skyBlue & cf.bold | self.description}"
        return string

    class Meta:
        database = db
