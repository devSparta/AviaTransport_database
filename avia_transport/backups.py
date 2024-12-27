import os
import subprocess
import datetime

db_name = "postgres"
db_user = "postgres"
db_password = "12345"
db_host = "127.0.0.1"
db_port = "5432"

backups_dir = r"C:\Users\nikbu\YandexDisk\backups"

def backup_database():
    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(backups_dir, f"{db_name}_backup_{current_time}.sql")

    pg_dump_path = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"

    pg_dump_command = [
        pg_dump_path,                  # Путь к pg_dump
        "-U", db_user,                 # Пользователь базы данных
        "-h", db_host,                 # Хост базы данных
        "-p", db_port,                 # Порт базы данных
        "-F", "c",                     # Формат резервной копии (сжатый)
        "-f", backup_file,             # Путь к файлу для резервной копии
        db_name                        # Имя базы данных
    ]

    env = os.environ.copy()
    env["PGPASSWORD"] = db_password

    try:
        subprocess.run(pg_dump_command, env=env, check=True)
        print(f"Резервная копия успешно создана: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании резервной копии: {e}")
    except Exception as ex:
        print(f"Непредвиденная ошибка: {ex}")

backup_database()
