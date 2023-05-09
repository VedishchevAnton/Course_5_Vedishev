"""Реализация класса HeadHunterAPI, для получения данных о вакансиях и работодателях с ресурса HeadHunter.ru"""
import requests


class HeadHunterAPI:
    def __init__(self):
        self.employer_data = None  # данные о работодателе
        self.url_hh = f"https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query):
        """
        Метод для получения вакансий с помощью HeadHunterApi.
        Search_query Ключевое слово для поиска вакансии.
        Return: Список объектов класса Vacancy.
        """
        params = {'text': search_query,
                  'per_page': 100,
                  'area': 113
                  }
        vacancies_data = []
        response = requests.get(self.url_hh, params)
        if response.status_code == 200:
            vacancies = response.json()["items"]
            for vacancy in vacancies:
                if vacancy['employer']['name'] == search_query:
                    if vacancy['salary'] is not None:
                        vacancy_data = {  # создаем словарь с данными о вакансии
                            'id_vacancy': vacancy['id'],  # идентификатор вакансии
                            'employer_id': vacancy['employer']['id'],
                            'vacancy_name': vacancy['name'],  # название вакансии
                            'description': vacancy['snippet']['responsibility'],  # описание вакансии
                            'area': vacancy['area']['name'],
                            'url': vacancy['alternate_url'],  # сайт вакансии
                            'salary_from': vacancy['salary']['from'],  # зарплата от
                            'salary_to': vacancy['salary']['to'],  # зарплата до
                            'currency': vacancy['salary']['currency'],  # валюта
                            'published_at': vacancy['published_at']  # дата публикации вакансии
                        }
                        vacancies_data.append(vacancy_data)
                        self.employer_data = HeadHunterAPI.get_employers(vacancy_data['employer_id'])
                    else:
                        continue
        else:
            print("Error:", response.status_code)

        return self.employer_data, vacancies_data

    @staticmethod
    def get_employers(employer_id):
        """
        Получает список вакансий по идентификатору работодателя.
        :param employer_id: Идентификатор работодателя
        :type employer_id: int
        :return: список вакансий
        """
        employers = []
        response_employers = requests.get(
            f'https://api.hh.ru/employers/{employer_id}')  # запрос на получение информации о работодателе
        if response_employers.ok:  # если запрос успешен
            data_employer = response_employers.json()  # получаем данные о работодателе в формате JSON
            employer = {  # создаем словарь с данными о работодателе
                'employer_id': data_employer['id'],  # идентификатор работодателя
                'name': data_employer['name'],  # название работодателя
                'url': data_employer['site_url']  # сайт работодателя
            }
            employers.append(employer)
        return employers

# # Пример использования функции
# hh = HeadHunterAPI()
# data_vac = hh.get_vacancies('Яндекс')
# print(data_vac)
