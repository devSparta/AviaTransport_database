from peewee import *
from config import db
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(Model):
    class Meta:
        database = db

class Flight(BaseModel):
    id = AutoField()
    depature_point = CharField(max_length=3, null=False)  # Код IATA (3 символа)
    arrival_point = CharField(max_length=3, null=False)   # Код IATA (3 символа)
    depature_time = DateTimeField(null=False)
    arrival_time = DateTimeField(null=False)

class Aviacompany(BaseModel):
    id = AutoField()
    name = CharField(max_length=100, null=False)
    planes_amount = IntegerField(null=False)

class Ticket(BaseModel):
    id = AutoField()
    cost = IntegerField(null=False)
    landing_class = CharField(max_length=20, null=False)
    flight_id = ForeignKeyField(Flight, backref='tickets', on_delete='CASCADE')

class Airplane(BaseModel):
    id = AutoField()
    business_seats = IntegerField(null=True)
    econom_seats = IntegerField(null=True)
    luggage_capacity = IntegerField(null=False)
    aviacompany_id = ForeignKeyField(Aviacompany, backref='airplanes', on_delete='CASCADE')
    flight_id = ForeignKeyField(Flight, backref='airplanes', on_delete='CASCADE')

class Client(BaseModel):
    id = AutoField()
    name = CharField(max_length=75, null=False)
    phone_number = CharField(max_length=20, null=False)
    flight_hours = IntegerField(null=True)
    luggage = IntegerField(null=True)
    aviacom_id = ForeignKeyField(Aviacompany, backref='client', on_delete='CASCADE')

    class Meta:
        constraints = [
            Check('substr(phone_number, 1, 2) = "+7"'),
            Check('right(phone_number, 10) ~ \'^[0-9]+$\''),
        ]

# Модель пользователя
class Users(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    role = IntegerField(null=True)
    email = CharField(null=True)# 1 - admin, 2 - user

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
