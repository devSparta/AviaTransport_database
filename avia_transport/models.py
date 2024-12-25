from peewee import *
from config import db  # Предполагается, что db настроен в config.py

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
    aviacompany_id = ForeignKeyField(Aviacompany, backref='clients', on_delete='CASCADE')

    class Meta:
        constraints = [
            Check('substr(phone_number, 1, 2) = "+7"'),  # Номер должен начинаться с "+7"
            Check('right(phone_number, 10) ~ \'^[0-9]+$\''),  # Последние 10 символов должны быть цифрами
        ]
