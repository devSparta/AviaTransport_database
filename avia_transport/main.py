from routers import app
from models import Flight, Aviacompany, Ticket, Airplane, Client, Users, db

if __name__ == '__main__':
    app.run(debug=True)
    with db:
        db.create_tables([Flight, Aviacompany, Ticket, Airplane, Client, Users])
