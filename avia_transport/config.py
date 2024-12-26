from flask import Flask
from peewee import *

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '4325436435'

db = PostgresqlDatabase(
          user='postgres',
          password='12345',
          host='127.0.0.1',
          port='5432',
          database='postgres'
                        )