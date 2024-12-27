from peewee import PostgresqlDatabase, CharField
import peewee_migrate
from config import db
migrator = peewee_migrate.Migrator(db)

migrator.drop_column('user', 'email', CharField(null=True))

migrator.run()

