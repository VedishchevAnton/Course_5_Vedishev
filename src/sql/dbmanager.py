import psycopg2
from src.sql.config_parser import config


class DBManager:
    def __init__(self, database_name: str):
        """
        Конструктор класса DBManager.
        :param database_name: имя базы данных для подключения
        """
        self._database = database_name
        self._connection = None

    def connect(self):
        """
        Функция устанавливает соединение с базой данных с использованием параметров из конфигурации.
        """
        params = config()
        params["database"] = self._database
        self._connection = psycopg2.connect(**params)

    def close(self):
        """
        Функция закрывает соединение с базой данных, если оно установлено.
        """
        if self._connection is not None:
            self._connection.close()

    def get_companies_and_vacancies_count(self):
        """
        Функция получает список всех компаний и количество вакансий у каждой компании
        """

        self.connect()
        cur = self._connection.cursor()
        cur.execute(
            "SELECT e.name AS company_name, COUNT(v.vacancy_id) AS vacancies_count "
            "FROM employers e LEFT JOIN vacancies v ON e.employer_id = v.employer_id "
            "GROUP BY e.name "
            "ORDER BY vacancies_count DESC;"
        )
        rows = cur.fetchall()
        for row in rows:
            print(f"{row}: {row} vacancies")
        cur.close()
        self.close()

    def get_all_vacancies(self):
        """
        Функция получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию
        """
        self.connect()
        cur = self._connection.cursor()
        cur.execute('''
        SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.currency, v.url
        FROM employers e
        JOIN vacancies v ON e.employer_id = v.employer_id;
        ''')
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
        self.close()

    def get_avg_salary(self):
        """
        Функция получает среднюю зарплату по вакансиям
        """
        self.connect()
        cur = self._connection.cursor()
        cur.execute("SELECT AVG((salary_from + salary_to) / 2) as average_salary FROM vacancies;")
        rows = cur.fetchall()
        print(f"Среднее значение 'зарплаты от': {rows}")
        cur.close()
        self.close()

    def get_vacancies_with_higher_salary(self):
        """
        Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        self.connect()
        cur = self._connection.cursor()
        cur.execute("SELECT * FROM vacancies WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)")
        rows = cur.fetchall()
        for row in rows:
            print(f"id: {row[0]} Вакансия: {row[2], row[3], row[4], row[5], row[6]}")
        cur.close()
        self.close()

    def get_vacancies_with_keyword(self, keyword):
        """
        Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова
        """
        self.connect()
        cur = self._connection.cursor()
        sql_query = "SELECT * FROM vacancies WHERE name LIKE %s"  # Формируем SQL запрос
        search_params = (f'%{keyword}%',)  # Задаем параметры поиска
        cur.execute(sql_query, search_params)  # Выполняем запрос с параметрам
        result = cur.fetchall()
        for row in result:
            print(f"id: {row[0]} Вакансия: {row[2], row[3], row[4], row[5], row[6]}")
        cur.close()
        self.close()


# Пример использования функции
# test = DBManager('my_database')
# test.get_companies_and_vacancies_count()
# test.get_all_vacancies()
# test.get_avg_salary()
# test.get_vacancies_with_higher_salary()
# test.get_vacancies_with_keyword('Менеджер')

