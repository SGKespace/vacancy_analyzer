import requests

def main():
    url = 'https://api.hh.ru/vacancies'
    search_text = 'Программист'
    params = {'text': f'{search_text}'}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    main()