import psycopg2


def create_tables():
    """Создание таблиц работодателей и вакансий."""
    # Устанавливаем соединение с базой данных
    conn = psycopg2.connect(host="localhost", database="test_1", user="postgres", password="231287")
    # Создаем объект-курсор для выполнения операций с базой данных
    with conn.cursor() as cursor:
        # Создаем таблицу employers
        cursor.execute("""
               CREATE TABLE employers (
                   employer_id SERIAL PRIMARY KEY,
                   name VARCHAR(255) NOT NULL,
                   url VARCHAR(255) NOT NULL
                );
           """)

        # Создаем таблицу vacancies
        cursor.execute("""
               CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    name VARCHAR NOT NULL,
                    description TEXT,
                    area VARCHAR(50) NOT NULL,
                    website VARCHAR(255),
                    salary_from INTEGER,
                    salary_to INTEGER,
                    published_at TIMESTAMP NOT NULL
                );
            """)
        conn.commit()
