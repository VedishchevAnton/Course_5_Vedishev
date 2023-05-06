from src.sql.config import user, password
import psycopg2


def create_database_and_tables(dbname: str) -> None:
    """
    Создает базу данных и таблицы в PostgreSQL.
    :param dbname str - имя базы данных.
    """
    try:
        # Подключение к серверу PostgreSQL
        conn = psycopg2.connect(database="postgres", user=user, password=password, host="localhost", port="5432")
        conn.autocommit = True
        cur = conn.cursor()

        # Проверка существования базы данных
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{dbname}'")
        if cur.fetchone():
            print(f"База данных {dbname} уже существует.")
            return

        # Создание базы данных
        cur.execute(f"CREATE DATABASE {dbname}")
        print(f"База данных {dbname} успешно создана.")
        cur.close()
        conn.close()

        # Подключение к созданной базе данных
        conn = psycopg2.connect(database=dbname, user=user, password=password, host="localhost", port="5432")
        cur = conn.cursor()

        # Создание таблиц employers и vacancies
        cur.execute("""
            CREATE TABLE employers (
                   employer_id SERIAL PRIMARY KEY,
                   name VARCHAR(255) NOT NULL,
                   url VARCHAR(255) NOT NULL
                );
        """)
        cur.execute("""
            CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    name VARCHAR NOT NULL,
                    description TEXT,
                    area VARCHAR(50) NOT NULL,
                    url VARCHAR(255),
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency VARCHAR(10),
                    published_at TIMESTAMP NOT NULL
                );
        """)

        # Применение изменений и закрытие соединения
        conn.commit()
        cur.close()
        conn.close()
        print("Таблицы успешно созданы.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка: {error}")

# # Пример использования функции
# create_database_and_tables("mydb")
