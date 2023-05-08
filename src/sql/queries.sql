# создание таблицы с работодателями
    CREATE TABLE employers (
                   employer_id SERIAL PRIMARY KEY,
                   name VARCHAR(255) NOT NULL,
                   url VARCHAR(255) NOT NULL
                );



# создание таблицы с вакансиями работодателей
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

# просмотр таблиц
SELECT * FROM employers;
SELECT * FROM vacancies;

# заполнение таблицы работодателей
    INSERT INTO employers (employer_id, name, url) VALUES (%s, %s, %s)

# заполнение таблицы вакансии
    INSERT INTO vacancies (employer_id, name, description, area, url, salary_from, salary_to, currency, published_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)

# получение списока всех компаний и количество вакансий у каждой компании
    SELECT e.name AS company_name, COUNT(v.vacancy_id) AS vacancies_count
    FROM employers e LEFT JOIN vacancies v ON e.employer_id = v.employer_id
    GROUP BY e.name
    ORDER BY vacancies_count DESC;

# получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
    SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.currency, v.url
    FROM employers e
    JOIN vacancies v ON e.employer_id = v.employer_id;

# получение средней зарплаты по вакансиям
    SELECT AVG((salary_from + salary_to) / 2) as average_salary FROM vacancies;

# получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
    SELECT AVG((salary_from + salary_to) / 2) as average_salary
    FROM vacancies;

# получение список всех вакансий, в названии которых содержатся переданные в метод слова
    SELECT * FROM vacancies WHERE name LIKE %s;