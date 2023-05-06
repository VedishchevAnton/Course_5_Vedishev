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

# заполнение таблицы работодателей (пример)
    INSERT INTO employers (name, url) VALUES
('Яндекс', 'https://yandex.ru/'),
('Mail.ru Group', 'https://corp.mail.ru/'),
('EPAM Systems', 'https://www.epam.com/');


# заполнение таблицы вакансии (пример)
    INSERT INTO vacancies (employer_id, name, description, area, url, salary_from, salary_to, currency, published_at) VALUES
(1, 'Data Scientist', 'Разработка алгоритмов машинного обучения', 'Москва', 'https://yandex.ru/jobs/vacancies/dev/data_scientist.html', 150000, 250000, 'RUB', '2023-05-01 10:00:00'),
(1, 'Backend-разработчик', 'Разработка и поддержка высоконагруженных сервисов', 'Санкт-Петербург', 'https://yandex.ru/jobs/vacancies/dev/backend_developer.html', 200000, 300000, 'RUB', '2023-05-02 11:00:00'),
(2, 'Data Engineer', 'Разработка и поддержка инфраструктуры для обработки больших данных', 'Москва', 'https://corp.mail.ru/ru/career/vacancy/166/', 180000, 280000, 'RUB', '2023-05-03 12:00:00'),
(2, 'Frontend-разработчик', 'Разработка пользовательских интерфейсов', 'Москва', 'https://corp.mail.ru/ru/career/vacancy/167/', 220000, 320000, 'RUB', '2023-05-04 13:00:00'),
(3, 'QA Automation Engineer', 'Разработка и поддержка автоматизированных тестов', 'Санкт-Петербург', 'https://www.epam.com/careers/job-listings/job.100006', 160000, 260000, 'RUB', '2023-05-05 14:00:00'),
(3, 'Java Developer', 'Разработка и поддержка корпоративных приложений', 'Москва', 'https://www.epam.com/careers/job-listings/job.100007', 200000, 300000, 'RUB', '2023-05-06 15:00:00');

