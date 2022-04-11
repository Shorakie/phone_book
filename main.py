import argparse

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
        app.start()
    except KeyboardInterrupt:
        pass

    print('Goodbye 👋.')

