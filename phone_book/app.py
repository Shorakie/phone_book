from pathlib import Path
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator
from phonenumbers import (parse as parse_phone_number,
                            format_number, PhoneNumberFormat)
import colorful as cf
import csv

from phonenumbers.phonenumberutil import is_valid_number

from .settings import db
from .validators import PhoneNumberValidator, RegexValidator, UniqueValidator
from .models import Contact


class App:
    def menu(self):
        """
        prompt main menu, contains following options:
        - add new contact
        - search contacts
        - import/export contacts
        """
        choices = [
                Choice(value='MENU_NEW_CONT', name='🧑 Add Contact'),
                Choice(value='MENU_SEARCH_CONT', name='🔎 Contacts List'),
                Choice(value='MENU_IMEXPORT', name='🔗 Import/Export Contacts'),
                Choice(value='MENU_EXIT', name='🚶 Exit'),
            ]

        return inquirer.select(
            message='Select an action:',
            choices=choices,
            mandatory_message='Please select an action',
        ).execute()

    def edit_contact(self, contact=Contact(first_name='', last_name=None, phone_number='', email=None, description=None), new=False):
        contact.first_name = inquirer.text(
            message='Contact first name 🧑:',
            default=contact.first_name,
            validate=lambda result: len(result) <=64 and len(result) >= 2,
            invalid_message="Name length should be between 2 and 64",
        ).execute()

        contact.last_name = inquirer.text(
            message='Contact last name 🧑:',
            default=contact.last_name if contact.last_name else '',
            mandatory=False,
            validate=lambda result: len(result) <=64 and len(result) >= 2,
            invalid_message="Name length should be between 2 and 64",
        ).execute()

        phone_number_validator = PhoneNumberValidator()
        if new:
            phone_number_validator &= UniqueValidator(Contact, Contact.phone_number)

        contact.phone_number = inquirer.text(
            message='Contact phone number 📱:',
            default=contact.phone_number,
            validate=phone_number_validator,
            transformer=lambda result: format_number(parse_phone_number(result, 'IR'), PhoneNumberFormat.E164),
            filter=lambda result: format_number(parse_phone_number(result, 'IR'), PhoneNumberFormat.E164),
        ).execute()

        contact.email = inquirer.text(
            message='Contact Email 📧:',
            default=contact.email if contact.email else '',
            mandatory=False,
            validate=RegexValidator(regex=r"^[-\w\.]+@([\w-]+\.)+[\w-]{2,4}$"),
        ).execute()

        contact.description = inquirer.text(
            message='Description about contact 📃:',
            default=contact.description if contact.description else '',
            mandatory=False,
            multiline=True,
        ).execute()

 
    def new_contact(self):
        choices = [
                Choice('NEW_CONT_SAVE', name='✅ Yes'),
                Choice('NEW_CONT_EDIT', name='📋 Edit'),
                Choice('NEW_CONT_CANCEL', name='❌ No'),
            ]

        action = 'NEW_CONT_EDIT'
        contact = Contact(first_name='', last_name='', phone_number='', email='', description='')
        while action == 'NEW_CONT_EDIT':
            self.edit_contact(contact, new=True)
            print(contact)
            action = inquirer.select(
                message='Save the contact?',
                choices=choices,
            ).execute()
        
        if action == 'NEW_CONT_SAVE':
            contact.save()


    def search_contacts(self):
        action = 'SEARCH_AGAIN'
        while action == 'SEARCH_AGAIN':
            # Select a contact
            choices = [Choice(contact, name=f"{contact.name}: {contact.phone_number}") for contact in Contact.select().order_by(Contact.last_name.asc(), Contact.first_name.asc())]
            if len(choices) == 0:
                print(f'{cf.bold & cf.red | "Error:"} There are no contacts in Database❗')
                break
            contact = inquirer.fuzzy(
                message="Select a contact",
                choices=choices,
                border=True,
                info=True,
                match_exact=True,
                max_height="50%",
            ).execute()

            print(contact)
            action = inquirer.select(
                message="Select an action",
                choices=[
                    Choice('SEARCH_EDIT', '📋 Edit'),
                    Choice('SEARCH_REMOVE', '❌ Remove'),
                    Choice('SEARCH_BACK', '↩ Back'),
                ]
            ).execute()
            
            if action == 'SEARCH_EDIT':
                self.edit_contact(contact)
                contact.save()
                action = 'SEARCH_AGAIN'
            elif action == 'SEARCH_REMOVE':
                if inquirer.confirm(
                        message=f'Remove {contact.name} from contacts?',
                    ).execute():
                    contact.delete_instance()
            elif action == 'SEARCH_BACK':
                return

    
    def export_contacts(self):
        field_names = ['name', 'phone_number', 'description']
        rows = [{
                'name': c.name,
                'phone_number': c.phone_number,
                'description': c.description
            } for c in Contact.select().order_by(Contact.last_name.asc(), Contact.first_name.asc())]

        export_path = inquirer.filepath(
            message='Enter file path to export:',
            default=str(Path.home()),
            validate=lambda result: '.' in result and result.split('.')[-1].lower()=='csv',
            invalid_message='Selected path is not a valid CSV file.',
            only_files=True,
            filter=lambda result:str(Path(result).resolve()),
        ).execute()

        with open(export_path, 'w+', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(rows)

        print(f'{cf.green & cf.bold | "Done exporting."}')


    def import_conacts(self):
        import_path = inquirer.filepath(
            message='Enter file path to impoert:',
            default=str(Path.home()),
            validate=PathValidator(is_file=True, message='Selected path is not a valid file'),
            only_files=True,
        ).execute()

        rows = []
        with open(import_path, 'r', encoding='UTF8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Validate the phone_number field from csv
                try:
                    if not is_valid_number(parse_phone_number(row['phone_number'])):
                        raise Exception()
                except:
                    continue

                # Format phone_number
                phone_number = format_number(parse_phone_number(row['phone_number'], 'IR'), PhoneNumberFormat.E164)
                # Check if the phone_number already exists
                if phone_number in [r['phone_number'] for r in rows] or Contact.select().where(Contact.phone_number==phone_number).exists():
                    continue

                rows.append({
                    'name': row['name'],
                    'phone_number': phone_number, 
                    'description': row['description'],
                })

        Contact.insert_many(rows).execute(db)

        print(f'{cf.green & cf.bold | "Done importing."}')


    def imexport_conacts(self):
        choices = [
            Choice(value='IMEX_IMPORT', name='📥 Import'),
            Choice(value='IMEX_EXPORT', name='📤 Export'),
        ]

        action = inquirer.select(
            message='Import or Export',
            choices=choices,
            mandatory_message='Please either select import or export',
        ).execute()
        
        
        if action == 'IMEX_IMPORT':
            self.import_conacts()
        elif action == 'IMEX_EXPORT':
            self.export_contacts()

    def start(self):
        menu_actions = {
            'MENU_NEW_CONT': self.new_contact,
            'MENU_SEARCH_CONT': self.search_contacts,
            'MENU_IMEXPORT': self.imexport_conacts,
        }

        while action := self.menu():
            # Break out of the loop if the action is Exit
            if action == 'MENU_EXIT':
                break

            # Execute the correct function for the action
            try:
                menu_actions[action]()
            except KeyboardInterrupt:
                continue

            # clear the screen
            # print('\33[H\33[J', end='')

app = App()

