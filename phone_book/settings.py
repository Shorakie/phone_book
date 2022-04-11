from peewee import SqliteDatabase
from smart_getenv import getenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = getenv('DB_NAME', default='contacts.db')
DEBUG = getenv('DEBUG', type=bool, default=False)

db = SqliteDatabase(DATABASE, pragmas={
                        'cache_size':-1024 * 64,
                        'foreign_keys': 1,
                        'journal_mode': 'wal',
                        'ignore_check_constraints': 0,
                    })

