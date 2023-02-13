import requests
import datetime
from dateutil.parser import parse
from itertools import count


def main():
    programming_languages = {'Java', 'Javascript', 'Python', 'Ruby', 'PHP', 'C++', 'C#'}
    list_count_programming_language = programming_language_count(programming_languages)
    print(list_count_programming_language)

def programming_language_count(programming_languages):
    language_counts = {}
    for programming_language in programming_languages:  # Бежим по списку языков
        search_text = f'Программист {programming_language}'
        count = 0
        town = 1
        url = 'https://api.hh.ru/vacancies'
        params = {'text': f'{search_text}', 'search_field': 'name', 'area': town}
        response = requests.get(url, params=params)
        response.raise_for_status()
        programming_language_vacancies = response.json()
        language_counts[f'{programming_language}'] = programming_language_vacancies['found']
    return language_counts


def get_hh_vacancies(search_text, town=1):  # Все вакансии Москвы
    url = 'https://api.hh.ru/vacancies'
    all_vacancies = []
    for page in count(0):
        params = {'text': f'{search_text}', 'search_field': 'name', 'area': town, 'page': page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        vacancies = response.json()
        all_vacancies.append(vacancies)
        if page >= vacancies['pages'] - 1:
            break
    return all_vacancies





if __name__ == '__main__':
    main()