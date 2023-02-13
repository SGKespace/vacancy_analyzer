import requests
import datetime
from dateutil.parser import parse
from itertools import count


def main():
    programming_languages = {'Java', 'Javascript', 'Python', 'Ruby', 'PHP', 'C++', 'C#'}
    search_text = 'Программист Python'
    vacancies = get_hh_vacancies(search_text, town=1)
    print(predict_rub_salary(vacancies))


def predict_rub_salary(vacancies):
    average_salary = []
    for vacancy_page in vacancies:
        for vacancy in vacancy_page['items']:
            salary = vacancy['salary']
            if not salary or salary['currency'] != 'RUR':
                continue
            payrol = calculation_payroll(salary['from'], salary['to'])
            average_salary.append(payrol)
    try:
        return sum(average_salary)//len(average_salary)
    except:
        return 0, 0


def calculation_payroll(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) // 2
    if salary_from and not salary_to:
        return int(salary_from * 1.2)
    if not salary_from and salary_to:
        return int(salary_to * 0.8)


def programming_language_salary(programming_languages):  # зарплаты
    language_salary = {}
    for programming_language in programming_languages:  # Бежим по списку языков
        search_text = f'{programming_language}'
        town = 1
        url = 'https://api.hh.ru/vacancies'
        params = {'text': f'{search_text}', 'search_field': 'name', 'area': town}
        response = requests.get(url, params=params)
        response.raise_for_status()
        programming_language_salary = response.json()
        cashh = {}
        for number, vacancie in enumerate(programming_language_salary['items']):
            cashh[number] = vacancie['salary']
            language_salary[f'{programming_language}'] = cashh
    return language_salary


def programming_language_count(programming_languages):
    language_counts = {}
    for programming_language in programming_languages:  # Бежим по списку языков
        search_text = f'{programming_language}'
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