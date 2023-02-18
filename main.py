import os
from itertools import count
from dotenv import load_dotenv

import requests
from terminaltables import AsciiTable


def main():
    """ Выводит в окно терминала статистику вакансий программиста по языкам программирования из двух
        популярных ресурсов поиска работы HeadHunter и SuperJob.
    """

    load_dotenv()
    superjob_token = os.environ['SUPERJOB_TOKEN']
    table_title = 'SuperJob Moscow'
    sj_statistic = get_statistics_sj(superjob_token)
    print_vacancies_statistic(sj_statistic, table_title)
    table_title = 'HeadHunter Moscow'
    hh_statistic = get_statistics_hh()
    print_vacancies_statistic(hh_statistic, table_title)


def print_vacancies_statistic(vacancies_stat, table_title):
    """ Вывод в консоль таблицы статистических данных
    :param vacancies_stat: Словарь с данными
    :param table_title: Заголовок таблицы
    :return: True
    """
    profession_statistics = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language, statistic in vacancies_stat.items():
        profession_statistics.append([language, statistic['vacancies_found'], statistic['vacancies_processed'], statistic['average_salary']])
    table = AsciiTable(profession_statistics)
    table.title = table_title
    print(table.table)


def get_statistics_sj(superjob_token):
    """ Статистика вакансий прогрммиста по языкам программирования из ресурса SuperJob
    :param superjob_token: Токен для доступа к API SuperJob
    :return programming_language_statistics:
    :rtype: dict
    """
    programming_languages = {'Java', 'Javascript', 'Python', 'Ruby', 'PHP', 'C++', 'C#'}
    programming_language_statistics = {}
    for programming_language in programming_languages:
        search_text = f'программист {programming_language}'
        vacancy_pages = get_sj_vacancies(search_text, superjob_token, town=4, count_on_page=20)
        statistic = get_salary_statistic_superjob(vacancy_pages)
        programming_language_statistics[programming_language] = statistic

    return programming_language_statistics


def get_salary_statistic_superjob(vacancy_pages):
    """ Статистика вакансий прогрммиста по языку программирования из ресурса SuperJob
    :param vacancy_pages:
    :return Статистику
    :rtype: dict
    """

    average_salary = []
    for vacancy_page in vacancy_pages:
        for vacancy in vacancy_page['objects']:
            if vacancy['currency'] != 'rub':
                continue
            salary = calculate_average_wage(vacancy['payment_from'], vacancy['payment_to'])
            if not salary:
                continue
            average_salary.append(salary)

    vacancies_found = vacancy_page['total']
    try:
        vacancies_processed = len(average_salary)
        average_salary = sum(average_salary)//len(average_salary)
    except ZeroDivisionError:
        vacancies_processed = 0
        average_salary = 0

    return {'vacancies_found': f'{vacancies_found}',
            'vacancies_processed': f'{vacancies_processed}',
             'average_salary': f'{average_salary}'
            }


def get_sj_vacancies(search_text, superjob_token, town=4, count_on_page=20):
    """ Вакансии прогрммиста по языку программирования из ресурса SuperJob
        :param search_text: Поисковая строка для запроса
        :param town: Город в котором ищем вакансии, по умолчанию Москва
        :param count_on_page: Максимальное количество вакансий на страницу в запросе
        :return vacancy_pages:
        :rtype: dict
    """

    keyword = search_text
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': f'{superjob_token}',
        'Content-Type': 'application / x - www - form - urlencoded'}
    vacancy_pages = []
    for page in count(0):
        params = {
            'town': town,
            'keywords': keyword,
            'page': page,
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancy_page = response.json()
        vacancy_pages.append(vacancy_page)
        if page >= vacancy_page['total'] / ((page + 1) * count_on_page):
            break
    return vacancy_pages


def get_statistics_hh():
    """ Вакансии прогрммиста по языкам программирования из ресурса HeadHunter
        :return programming_language_statistics:
        :rtype: dict
        """

    programming_languages = {'Java', 'Javascript', 'Python', 'Ruby', 'PHP', 'C++', 'C#'}
    programming_language_statistics = {}

    for programming_language in programming_languages:
        search_text = f'{programming_language}'
        vacancies = get_hh_vacancies(search_text, town=1)
        current_salary = get_salary_statistic_hh(vacancies)
        programming_language_statistics[programming_language] = current_salary
    return programming_language_statistics


def get_salary_statistic_hh(vacancies):
    """ Статистика заработных плат
        :param vacancies: Вакансии программиста по языку программирования
        :return Количество вакансий, средняя заработная пплата
        :rtype: dict
    """

    average_salary = []
    for vacancy_page in vacancies:
        for vacancy in vacancy_page['items']:
            salary = vacancy['salary']
            if not salary or salary['currency'] != 'RUR':
                continue
            payrol = calculate_average_wage(salary['from'], salary['to'])
            average_salary.append(payrol)

    vacancies_found = vacancy_page['found']

    try:
        vacancies_processed = len(average_salary)
        average_salary = sum(average_salary)//len(average_salary)
    except ZeroDivisionError:
        vacancies_processed = 0
        average_salary = 0
    return {'vacancies_found': f'{vacancies_found}',
            'vacancies_processed': f'{vacancies_processed}',
            'average_salary': f'{average_salary}'
            }


def calculate_average_wage(salary_from, salary_to):
    """ Подсчет средней заработной платы в вакансии
        :param salary_from: Минимальная заявленная оплата
        :param salary_to: Максимальная заявленная оплата
        :return Количество вакансий в оценке, средняя заработная пплата
        :rtype: dict
    """

    if salary_from and salary_to:
        return (salary_from + salary_to) // 2
    if salary_from and not salary_to:
        return int(salary_from * 1.2)
    if not salary_from and salary_to:
        return int(salary_to * 0.8)


def get_hh_vacancies(search_text, town=1):
    """ Вакансии прогрммиста по языку программирования из ресурса HeadHunter
            :param search_text: Поисковая строка для запроса
            :param town: Город в котором ищем вакансии, по умолчанию Москва
            :return all_vacancies: Вакансии
            :rtype: dict
    """

    url = 'https://api.hh.ru/vacancies'
    all_vacancies = []
    for page in count(0):
        params = {'text': f'{search_text}', 'search_field': 'name', 'area': town, 'page': page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        vacancy_page = response.json()
        all_vacancies.append(vacancy_page)
        if page >= vacancy_page['pages'] - 1:
            break
    return all_vacancies


if __name__ == '__main__':
    main()