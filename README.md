# main
Скрипт анализа вакансий программиста в Москве по востребованным языкам программирования ([Рейтинг языков по версии Github](https://habr.com/ru/post/310262/)) с HeadHunter и SuperJob.
[Общая информация по API hh.ru](https://github.com/hhru/api/blob/master/docs/general.md)  и   [API SuperJob](https://api.superjob.ru/) - Требуется регистрация для получения Secret key, который потом указывается в .env.

# Переменные окружения
Пример файла .env
``` 
SUPERJOB_TOKEN='v3.r.12345678.dfethrg4h56njmrhgsvgf5y6g5ewvwg.dfknejf3iuhuytfbkjsbcjwtrugknxkdcbuwhdlq8743hfkwbk'
```

## Требования к окружению

Python 3.xx и выше (должен быть уже установлен)

requests == 2.24.0

python-dotenv == 0.21.1

terminaltables == 3.1.10


Можно установить командой  
``` 
PIP install -r requirements.txt
```

# Пример запуск скрипта
Для того чтобы запустить скрипт, войдите в директорию со скриптом и запустите команду:
```
python main.py
```

Пример успешного запуска скрипта:
```
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Java                  | 6                | 4                   | 146250           |
| Python                | 19               | 18                  | 81448            |
| Ruby                  | 0                | 0                   | 0                |
| C++                   | 16               | 15                  | 163800           |
| C#                    | 4                | 4                   | 99250            |
| Javascript            | 30               | 29                  | 96261            |
| PHP                   | 11               | 9                   | 166102           |
+-----------------------+------------------+---------------------+------------------+
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Java                  | 916              | 114                 | 251247           |
| Python                | 585              | 133                 | 180568           |
| Ruby                  | 47               | 18                  | 256115           |
| C++                   | 442              | 104                 | 203508           |
| C#                    | 368              | 96                  | 191457           |
| Javascript            | 352              | 112                 | 196415           |
| PHP                   | 559              | 247                 | 179291           |
+-----------------------+------------------+---------------------+------------------+

```


## Отказ от ответственности

Автор программы не несет никакой ответственности за то, как вы используете этот код или как вы используете сгенерированные с его помощью данные. Эта программа была написана для обучения автора и других целей не несет. Не используйте данные, сгенерированные с помощью этого кода в незаконных целях.
