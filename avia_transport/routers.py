from config import *
from models import *
from flask import Flask, render_template, request
from peewee import DoesNotExist
from functools import wraps
from flask import session, redirect, url_for

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 2)  # Default role is 'user'

        # Проверка на уникальность username
        if Users.select().where(Users.username == username).exists():
            return "Username already exists", 400

        # Создание пользователя с хешированным паролем
        user = Users(username=username, role=role)
        user.set_password(password)
        user.save()

        return redirect('/login')  # После регистрации редирект на страницу логина

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Поиск пользователя по имени
        user = Users.get_or_none(Users.username == username)

        # Если пользователь найден и пароль совпадает
        if user and user.check_password(password):
            session['user_id'] = user.id  # Сохраняем ID пользователя в сессии
            session['role'] = user.role    # Сохраняем роль пользователя

            if session['role'] == 1:
                return redirect('/admin_dashboard')
            else:
                return redirect('/dashboard')

        return "Invalid username or password", 400

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect('/login')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 1:
            return redirect(url_for('login'))  # Если пользователь не администратор, перенаправляем на страницу логина
        return f(*args, **kwargs)
    return decorated_function

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
@admin_required
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
@admin_required
def delete_client(client_id):
    client = Client.get(Client.id == client_id)
    client.delete_instance()
    return redirect('/clients')

@app.route('/update_client/<int:client_id>', methods=['GET', 'POST'])
@admin_required
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

@app.route('/add_flight', methods=['POST'])
@admin_required
def add_flight():
    id = request.form['id']
    depature_point = request.form['depature_point']
    arrival_point = request.form['arrival_point']
    depature_time = request.form['depature_time']
    arrival_time = request.form['arrival_time']

    Flight.create(
        id=id,
        depature_point=depature_point,
        arrival_point=arrival_point,
        depature_time=depature_time,
        arrival_time=arrival_time
    )

    return redirect('/flights')

@app.route('/delete_flight/<int:flight_id>', methods=['POST'])
@admin_required
def delete_flight(flight_id):
    flight = Flight.get(Flight.id == flight_id)
    flight.delete_instance()
    return redirect('/flights')

@app.route('/update_flight/<int:flight_id>', methods=['GET', 'POST'])
@admin_required
def update_flight(flight_id):
    flight = Flight.get(Flight.id == flight_id)

    if request.method == 'GET':
        return render_template('update_flight.html', flight=flight)

    else:
        flight.depature_point = request.form['depature_point']
        flight.arrival_point = request.form['arrival_point']
        flight.depature_time = request.form['depature_time']
        flight.arrival_time = request.form['arrival_time']
        flight.save()
        return redirect('/flights')


@app.route('/delete_aviacompany/<int:aviacompany_id>', methods=['POST'])
@admin_required
def delete_aviacompany(aviacompany_id):
    company = Aviacompany.get(Aviacompany.id == aviacompany_id)
    company.delete_instance()
    return redirect('/aviacompanies')

@app.route('/update_aviacompany/<int:aviacompany_id>', methods=['GET', 'POST'])
@admin_required
def update_aviacompany(aviacompany_id):
    company = Aviacompany.get(Aviacompany.id == aviacompany_id)

    if request.method == 'GET':
        return render_template('update_aviacompany.html', company=company)

    else:
        company.name = request.form['name']
        company.planes_amount = request.form['planes_amount']
        company.save()
        return redirect('/aviacompanies')

@app.route('/add_aviacompany', methods=['POST'])
@admin_required
def add_aviacompany():
    id = request.form['id']
    name = request.form['name']
    planes_amount = request.form['planes_amount']

    # Создаем новую авиакомпанию
    Aviacompany.create(
        id=id,
        name=name,
        planes_amount=planes_amount
    )

    return redirect('/aviacompanies')

@app.route('/add_ticket', methods=['POST'])
@admin_required
def add_ticket():
    id = request.form['id']
    cost = request.form['cost']
    landing_class = request.form['landing_class']
    flight_id = request.form['flight_id']

    # Проверка, существует ли рейс с таким id
    try:
        flight = Flight.get(Flight.id == flight_id)
    except Flight.DoesNotExist:
        return f"Flight with id {flight_id} does not exist!", 400

    # Создание нового билета
    Ticket.create(
        id=id,
        cost=cost,
        landing_class=landing_class,
        flight_id=flight_id
    )

    return redirect('/tickets')

@app.route('/update_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@admin_required
def update_ticket(ticket_id):
    ticket = Ticket.get(Ticket.id == ticket_id)

    if request.method == 'GET':  # Если GET-запрос, показываем форму с текущими данными
        flights = Flight.select()  # Список всех рейсов для выбора
        return render_template('update_ticket.html', ticket=ticket, flights=flights)

    else:  # Если POST-запрос, обновляем данные билета
        ticket.cost = request.form['cost']
        ticket.landing_class = request.form['landing_class']
        ticket.flight_id = request.form['flight_id']

        # Сохраняем изменения
        ticket.save()

        return redirect('/tickets')  # Перенаправляем на страницу со списком билетов

@app.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@admin_required
def delete_ticket(ticket_id):
    ticket = Ticket.get(Ticket.id == ticket_id)
    ticket.delete_instance()  # Удаление билета
    return redirect('/tickets')

@app.route('/add_airplane', methods=['POST'])
@admin_required
def add_airplane():
    # Получаем данные из формы
    id = request.form['id']
    business_seats = request.form['business_seats']
    econom_seats = request.form['econom_seats']
    luggage_capacity = request.form['luggage_capacity']
    aviacompany_id = request.form['aviacompany_id']
    flight_id = request.form['flight_id']

    # Создаем новый самолет
    Airplane.create(
        id=id,
        business_seats=business_seats,
        econom_seats=econom_seats,
        luggage_capacity=luggage_capacity,
        aviacompany_id=aviacompany_id,
        flight_id=flight_id
    )

    # Перенаправляем на страницу со всеми самолетами
    return redirect('/airplanes')

@app.route('/delete_airplane/<int:airplane_id>', methods=['POST'])
@admin_required
def delete_airplane(airplane_id):
    # Получаем самолет по ID
    airplane = Airplane.get(Airplane.id == airplane_id)

    # Удаляем самолет
    airplane.delete_instance()

    # Перенаправляем на страницу со всеми самолетами
    return redirect('/airplanes')

@app.route('/update_airplane/<int:airplane_id>', methods=['GET', 'POST'])
@admin_required
def update_airplane(airplane_id):
    airplane = Airplane.get(Airplane.id == airplane_id)  # Получаем самолет по ID

    if request.method == 'GET':  # Если GET-запрос, показываем форму с текущими данными самолета
        return render_template('update_airplane.html', airplane=airplane)

    else:  # Если POST-запрос, обновляем данные самолета
        airplane.business_seats = request.form['business_seats']
        airplane.econom_seats = request.form['econom_seats']
        airplane.luggage_capacity = request.form['luggage_capacity']
        airplane.aviacompany_id = request.form['aviacompany_id']
        airplane.flight_id = request.form['flight_id']
        airplane.save()  # Сохраняем изменения в базе данных

        # Перенаправляем на страницу со всеми самолетами
        return redirect('/airplanes')

@app.route('/dashboard')
def dashboard():
    if session['role'] == 2:  # Проверяем, что пользователь обычный
        return render_template('dashboard.html')  # Страница для обычного пользователя
    return redirect('/logout')  # Если пользователь не обычный, перенаправляем на страницу выхода

@app.route('/admin_dashboard')
def admin_dashboard():
    if session['role'] == 1:  # Проверяем, что пользователь администратор
        return render_template('admin_dashboard.html')  # Страница для админа
    return redirect('/logout')  # Если пользователь не администратор, перенаправляем на страницу выхода

@app.route('/flights_view')
def get_flights_view():
    flights = Flight.select()
    return render_template("flights_view.html", flights=flights)


@app.route('/aviacompanies_view')
def get_aviacompanies_view():
    aviacompanies = Aviacompany.select()
    return render_template("aviacompanies_view.html", aviacompanies=aviacompanies)


@app.route('/tickets_view')
def get_tickets_view():
    tickets = Ticket.select()
    return render_template("tickets_view.html", tickets=tickets)


@app.route('/airplanes_view')
def get_airplanes_view():
    airplanes = Airplane.select()
    return render_template("airplanes_view.html", airplanes=airplanes)


@app.route('/clients_view', methods=['GET'])
def get_clients_view():
    aviacompanies = Aviacompany.select()  # Получаем все авикомпании
    clients = Client.select()  # Получаем всех клиентов
    return render_template('client_view.html', client=clients, aviacompanies=aviacompanies)
