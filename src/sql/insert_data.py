import psycopg2
from src.sql.config import user, password
from src.headhunter_api import HeadHunterAPI


def insert_data(dbname: str, search_query) -> None:
    """
    Вставляет данные о работодателях и вакансиях в базу данных.
    :param search_query: запрос по работодателю
    :param dbname: имя базы данных
    """
    # Подключение к базе данных
    conn = psycopg2.connect(database=dbname, user=user, password=password, host="localhost", port="5432")
    cur = conn.cursor()
    hh_api = HeadHunterAPI()
    employers_data, vacancies_data = hh_api.get_vacancies(search_query)
    # Вставка данных о работодателях
    for employer in employers_data:
        cur.execute("INSERT INTO employers (employer_id, name, url) VALUES (%s, %s, %s)",
                    (employer['employer_id'], employer['name'], employer['url']))

    # Вставка данных о вакансиях
    for vacancy in vacancies_data:
        cur.execute(
            "INSERT INTO vacancies "
            "(employer_id, name, description, area, url, salary_from, salary_to, currency, published_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (vacancy['employer_id'], vacancy['vacancy_name'], vacancy['description'], vacancy['area'], vacancy['url'],
             vacancy['salary_from'], vacancy['salary_to'], vacancy['currency'], vacancy['published_at']))

    # Фиксация изменений и закрытие соединения с базой данных
    conn.commit()
    cur.close()
    conn.close()

# Пример использования функции
# db_input = input('Введите название базы данных: ')
# employer_input = input('Введите название компаний , для получения вакансий: ')
# insert_data('finally_test', 'Авито')
