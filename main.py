import requests
import datetime
from dateutil.parser import parse
from itertools import count
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    superjob_token = os.environ['SUPERJOB_TOKEN']
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': f'{superjob_token}',
        'Content-Type': 'application / x - www - form - urlencoded'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    vacancy_page = response.json()['objects']
    for vacancie in vacancy_page:
       print(vacancie['profession'])


def programming_languages_statistic(): # общая статистика хх ру
    programming_languages = {'Java', 'Javascript', 'Python', 'Ruby', 'PHP', 'C++', 'C#'}
    programming_language_counts = programming_language_count(programming_languages)  # количество вакансий
    programming_salarys = {}
    for programming_language in programming_languages:
        search_text = f'{programming_language}'
        vacancies = get_hh_vacancies(search_text, town=1)
        current_salary = predict_rub_salary(vacancies)
        programming_salarys[programming_language] = {"vacancies_processed": current_salary[0], "average_salary": current_salary[1]}


    programming_language_statistics = {}
    for language in programming_language_counts:
        programming_language_statistics[language] = {'vacancies_found': programming_language_counts[language],
                                                     'vacancies_processed': programming_salarys[language][
                                                         'vacancies_processed'],
                                                     'average_salary': programming_salarys[language]['average_salary']}

    print(programming_language_statistics)
    return programming_language_statistics



def predict_rub_salary(vacancies):  # средняя зарплата по вакансии - как сформирована
    average_salary = []
    for vacancy_page in vacancies:
        for vacancy in vacancy_page['items']:
            salary = vacancy['salary']
            if not salary or salary['currency'] != 'RUR':
                continue
            payrol = calculation_payroll(salary['from'], salary['to'])
            average_salary.append(payrol)
    try:
        return len(average_salary), sum(average_salary)//len(average_salary)
    except:
        return 0, 0


def calculation_payroll(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) // 2
    if salary_from and not salary_to:
        return int(salary_from * 1.2)
    if not salary_from and salary_to:
        return int(salary_to * 0.8)


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