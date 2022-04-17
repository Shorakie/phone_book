import argparse

import colorful as cf

from phone_book.app import app
from phone_book.models import Contact
from phone_book.utils import insert_fake

def parseArgs():
    parser = argparse.ArgumentParser('Phone number book')
    parser.add_argument('--fake', type=int, default=0)
    args = parser.parse_args()

    # insert fake contacts for test
    if args.fake:
        insert_fake(args.fake)

if __name__ == "__main__":
    # Create Contacts table in database if it doesn't exist
    Contact.create_table(True)

    # Clear the screen
    print('\33[H\33[J', end='')

    parseArgs()

    # Start the app by showing main menu
    try:
        print(f'You can skip {cf.deepSkyBlue & cf.bold | "questions"} with {cf.orange & cf.bold | "Ctrl+Z"}!')
        print(f'You can cancel {cf.deepSkyBlue & cf.bold | "current action"} with {cf.orange & cf.bold | "Ctrl+C"}!')
        app.start()
    except KeyboardInterrupt:
        pass

    print(cf.lightCoral & cf.bold | 'Goodbye' ,'👋.')

