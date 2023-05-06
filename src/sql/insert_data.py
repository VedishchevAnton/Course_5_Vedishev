import psycopg2
from src.sql.config import user, password


def insert_data(dbname: str, employers_data, vacancies_data) -> None:
    """
    Вставляет данные о работодателях и вакансиях в базу данных.
    :param dbname: имя базы данных
    :param employers_data: список словарей с данными о работодателях
    :param vacancies_data: список словарей с данными о вакансиях
    """
    # Подключение к базе данных
    conn = psycopg2.connect(database=dbname, user=user, password=password, host="localhost", port="5432")
    cur = conn.cursor()

    # Вставка данных о работодателях
    for employer in employers_data:
        cur.execute("INSERT INTO employers (name, url) VALUES (%s, %s)", (employer['name'], employer['url']))

    # Вставка данных о вакансиях
    for vacancy in vacancies_data:
        cur.execute(
            "INSERT INTO vacancies "
            "(employer_id, name, description, area, website, salary_from, salary_to, published_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (vacancy['employer_id'], vacancy['name'], vacancy['description'], vacancy['area'], vacancy['website'],
             vacancy['salary_from'], vacancy['salary_to'], vacancy['published_at']))

    # Фиксация изменений и закрытие соединения с базой данных
    conn.commit()
    cur.close()
    conn.close()
