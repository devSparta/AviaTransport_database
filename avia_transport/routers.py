from config import *
from models import *
from flask import render_template
from flask import request
from flask import redirect


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


@app.route('/clients', methods=['GET'])
def get_clients():
    aviacompanies = Aviacompany.select()  # Получаем все авикомпании
    clients = Client.select()  # Получаем всех клиентов
    return render_template('client.html', client=clients, aviacompanies=aviacompanies)



@app.route('/add_client', methods=['POST'])
def add_client():
    id = request.form['id']
    name = request.form['name']
    phone_number = request.form['phone_number']
    flight_hours = request.form.get('flight_hours') or None
    luggage = request.form.get('luggage') or None
    aviacompany_id = request.form.get('aviacompany_id')

    # Если aviacompany_id не передано, вернем ошибку
    if not aviacompany_id:
        return "Aviacompany ID is required!", 400

    try:
        aviacompany = Aviacompany.get(Aviacompany.id == aviacompany_id)
    except Aviacompany.DoesNotExist:
        return f"Aviacompany with id {aviacompany_id} does not exist!", 400

    # Создаем нового клиента с привязкой к aviacompany_id
    Client.create(
        id = id,
        name=name,
        phone_number=phone_number,
        flight_hours=flight_hours,
        luggage=luggage,
        aviacom_id=aviacompany_id  # Сохраняем id авиакомпании
    )

    return redirect('/clients')



@app.route('/delete_client/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.get(Client.id == client_id)
    client.delete_instance()
    return redirect('/clients')

@app.route('/update_client/<int:client_id>', methods=['GET', 'POST'])
def update_client(client_id):
    client = Client.get(Client.id == client_id)  # Получаем клиента по ID

    if request.method == 'GET':  # Если GET-запрос, показываем форму с текущими данными клиента
        return render_template('update_client.html', client=client)

    else:  # Если POST-запрос, обновляем данные клиента
        client.name = request.form['name']
        client.phone_number = request.form['phone_number']
        client.flight_hours = request.form.get('flight_hours') or None
        client.luggage = request.form.get('luggage') or None
        client.aviacompany_id = request.form['aviacompany_id']
        client.save()  # Сохраняем изменения в базе данных
        return redirect('/clients')  # Перенаправляем на страницу со списком клиентов

