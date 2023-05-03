"""Реализация класса HeadHunterAPI, для получения данных о вакансиях и работодателях с ресурса HeadHunter.ru"""
import requests


class HeadHunterAPI:
    def __init__(self):
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
                            'employer': vacancy['employer']['name'],
                            'vacancy_name': vacancy['name'],  # название вакансии
                            'description': vacancy['snippet']['responsibility'],  # описание вакансии
                            'salary': vacancy['salary'],  # зарплата
                            'published_at': vacancy['published_at']  # дата публикации вакансии
                        }
                        vacancies_data.append(vacancy_data)
                    else:
                        continue
        else:
            print("Error:", response.status_code)
        return vacancies_data

    @staticmethod
    def get_employers(employer_id):
        """
        Получает список вакансий по идентификатору работодателя.
        :param employer_id: Идентификатор работодателя
        :type employer_id: int
        :return: список вакансий
        """
        employers = []  # список работодателей
        response_employers = requests.get(
            f'https://api.hh.ru/employers/{employer_id}')  # запрос на получение информации о работодателе
        if response_employers.ok:  # если запрос успешен
            data_employer = response_employers.json()  # получаем данные о работодателе в формате JSON
            employer = {  # создаем словарь с данными о работодателе
                'id_company': data_employer['id'],  # идентификатор работодателя
                'employer_name': data_employer['name'],  # название работодателя
                'description': data_employer['description'],  # описание работодателя
                'site': data_employer['site_url']  # сайт работодателя
            }
            employers.append(employer)
        return employers


hh = HeadHunterAPI()
vac = hh.get_employers(80)
# print(vac)
vac_2 = hh.get_vacancies('Яндекс')
# print(vac_2)
