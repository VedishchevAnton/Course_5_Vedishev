import psycopg2
from src.sql.config import user, password


class MyDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user=user,
            password=password
        )

    def get_companies_and_vacancies_count(self):
        """
        Функция получает список всех компаний и количество вакансий у каждой компании
        """

        cur = self.conn.cursor()
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
        self.conn.close()

    def get_all_vacancies(self):
        """
        Функция получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию
        """
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.currency, v.url
        FROM employers e
        JOIN vacancies v ON e.employer_id = v.employer_id;
        ''')
        all_vacancies = cursor.fetchall()
        cursor.close()
        return all_vacancies

    def get_avg_salary(self):
        """
        Функция получает среднюю зарплату по вакансиям
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT AVG((salary_from + salary_to) / 2) as average_salary "
                       "FROM vacancies;")
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM vacancies
        WHERE (salary_from + salary_to) / 2 > (
            SELECT AVG((salary_from + salary_to) / 2) FROM vacancies
        );
        """)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова
        """
        cursor = self.conn.cursor()
        cursor.execute(f"""SELECT * FROM vacancies 
        WHERE name LIKE %{keyword}%;""")
        result = cursor.fetchall()
        cursor.close()
        return result
