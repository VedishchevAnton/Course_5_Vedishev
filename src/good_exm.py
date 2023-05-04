import requests
import json
import psycopg2


# Метод для получения данных с помощью HeadHunterApi.
def get_vacancies(company_id):
    url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


# Устанавливаем соединение с базой данных
conn = psycopg2.connect(host="localhost", database="test_1", user="postgres", password="231287")

# Создаем объект-курсор для выполнения операций с базой данных
cursor = conn.cursor()

# Создание таблицы с работодателями
cursor.execute("""
CREATE TABLE IF NOT EXISTS employers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company_id INTEGER UNIQUE NOT NULL
);
""")
# Создание таблицы с вакансиями
cursor.execute("""
CREATE TABLE IF NOT EXISTS vacancies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    employer_id INTEGER REFERENCES employers(id),
    salary_min INTEGER,
    salary_max INTEGER,
    currency VARCHAR(10)
);
""")

conn.commit()

# Добавьте интересующие вас компании в таблицу employers:
companies = [
    {"name": "Яндекс", "company_id": 1740},
    {"name": "VK", "company_id": 15748},
    {"name": "Авито ", "company_id": 84585},
    {"name": "Delivery Club ", "company_id": 592442},
    {"name": "Сбер ", "company_id": 3529},
    {"name": "Ланит ", "company_id": 733},
    {"name": "ТЕНЗОР ", "company_id": 67611},
    {"name": "Альфа Банк ", "company_id": 80},
    {"name": "Carprice ", "company_id": 1532045},
    {"name": "USETECH ", "company_id": 681672}
]

for company in companies:
    cursor.execute("INSERT INTO employers (name, company_id) VALUES (%s, %s)", (company["name"], company["company_id"]))

conn.commit()

# Получите данные о вакансиях для каждой компании и добавьте их в таблицу vacancies:
cursor.execute("SELECT id, company_id FROM employers")
employers = cursor.fetchall()

for employer_id, company_id in employers:
    vacancies = get_vacancies(company_id)
    if vacancies:
        for vacancy in vacancies["items"]:
            title = vacancy["name"]
            salary_min = vacancy["salary"]["from"] if vacancy["salary"] else None
            salary_max = vacancy["salary"]["to"] if vacancy["salary"] else None
            currency = vacancy["salary"]["currency"] if vacancy["salary"] else None

            cursor.execute("""
                INSERT INTO vacancies (title, employer_id, salary_min, salary_max, currency)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, employer_id, salary_min, salary_max, currency))

conn.commit()

# Закройте соединение с базой данных:
cursor.close()
conn.close()
