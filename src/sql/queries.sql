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
                    published_at TIMESTAMP NOT NULL
                );

# заполнение таблицы с работодателями
    INSERT INTO employers (name, url)
    VALUES (%s, %s);


# заполнение таблицы с вакансиями работодателей
    INSERT INTO vacancies (employer_id, name, description, area, url, salary_from, salary_to, published_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);