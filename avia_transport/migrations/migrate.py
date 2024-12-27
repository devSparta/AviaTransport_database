from peewee import PostgresqlDatabase, CharField
import peewee_migrate
from config import db

# Создаем объект мигратора
migrator = peewee_migrate.Migrator(db)

# Добавляем новый столбец "email" в таблицу "users"
migrator.drop_column('user', 'email', CharField(null=True))

# Применяем миграцию
migrator.run()

