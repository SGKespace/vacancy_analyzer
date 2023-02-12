import requests
import datetime
from dateutil.parser import parse
from itertools import count


def main():
    hh_vacancies = get_hh_vacancies()
    city_ = 'Москва'
    all_Moscow_vacancies=[]
    for page_number, current_page in enumerate(hh_vacancies):
        for vacance in current_page['items']:
            if vacance['area']['name'] == city_:
                all_Moscow_vacancies.append(vacance)
                print(vacance)

    current_month = datetime.date.today().month
    current_month_Moscow_vacancies = []
    for vacance in all_Moscow_vacancies:
        if current_month == parse(vacance['published_at']).month:
            current_month_Moscow_vacancies.append(vacance)
    return all_Moscow_vacancies, current_month_Moscow_vacancies


def get_hh_vacancies(town=1):
    url = 'https://api.hh.ru/vacancies'
    search_text = 'Программист'
    all_vacancies = []

    for page in count(0):
        params = {'text': f'{search_text}', 'search_field': 'name', 'area': town, 'page': page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        vacancies = response.json()
        if page >= vacancies['pages'] - 1:
            break
        all_vacancies.append(vacancies)

    return all_vacancies


if __name__ == '__main__':
    main()