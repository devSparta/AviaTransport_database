from flask import Flask
from peewee import *

app = Flask(__name__)
app.config.from_object(__name__)

db = PostgresqlDatabase(
          user='postgres',
          password='12345',
          host='127.0.0.1',
          port='5432',
          database='postgres'
                        )