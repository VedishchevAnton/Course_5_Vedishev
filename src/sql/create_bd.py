import psycopg2
from src.sql.config_parser import config


def create_database_and_tables(dbname: str, ) -> None:
    """
    Создает базу данных и таблицы в PostgreSQL.
    :param dbname str - имя базы данных.
    """
    try:
        # Подключение к серверу PostgreSQL
        params = config()
        conn = psycopg2.connect(dbname='postgres', **params)
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
        params['dbname'] = dbname
        conn = psycopg2.connect(**params)
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
        print("Таблицы employers и vacancies успешно созданы.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка: {error}")


# Пример использования функции
create_database_and_tables("my_database")
