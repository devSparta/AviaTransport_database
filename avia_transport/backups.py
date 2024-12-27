import os
import subprocess
import datetime

# Конфигурация базы данных
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"

# Папка для резервных копий
BACKUP_FOLDER = r"C:\Users\nikbu\YandexDisk\backups"

def backup_database():
    # Проверка, существует ли папка для бэкапов, если нет - создаем
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    # Формирование имени файла для резервной копии
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(BACKUP_FOLDER, f"{DB_NAME}_backup_{current_time}.sql")

    # Путь к pg_dump
    pg_dump_path = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"

    # Формируем команду для pg_dump
    pg_dump_command = [
        pg_dump_path,                  # Путь к pg_dump
        "-U", DB_USER,                 # Пользователь базы данных
        "-h", DB_HOST,                 # Хост базы данных
        "-p", DB_PORT,                 # Порт базы данных
        "-F", "c",                     # Формат резервной копии (сжатый)
        "-f", backup_file,             # Путь к файлу для резервной копии
        DB_NAME                        # Имя базы данных
    ]

    # Устанавливаем переменную окружения для пароля
    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD

    try:
        # Выполняем команду
        subprocess.run(pg_dump_command, env=env, check=True)
        print(f"Резервная копия успешно создана: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании резервной копии: {e}")
    except Exception as ex:
        print(f"Непредвиденная ошибка: {ex}")

# Запуск функции бэкапа
backup_database()
