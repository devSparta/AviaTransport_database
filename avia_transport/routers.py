from config import *
from models import *
from flask import render_template

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/flights')
def get_flights():
    flights = Flight.select()
    return render_template("flights.html", flights=flights)


@app.route('/aviacompanies')
def get_aviacompanies():
    aviacompanies = Aviacompany.select()
    return render_template("aviacompanies.html", aviacompanies=aviacompanies)


@app.route('/tickets')
def get_tickets():
    tickets = Ticket.select()
    return render_template("tickets.html", tickets=tickets)


@app.route('/airplanes')
def get_airplanes():
    airplanes = Airplane.select()
    return render_template("airplanes.html", airplanes=airplanes)


@app.route('/clients')
def get_clients():
    clients = Client.select()
    return render_template("clients.html", clients=clients)
