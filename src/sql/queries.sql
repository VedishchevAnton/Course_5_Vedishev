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
