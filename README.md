# tz_NtPro
Ссылка на тестовое --> https://drive.google.com/file/d/1qaPZ0fxuuMgYcZ2ds_8oqYFYFqRdn3tf/view?usp=sharing  

## Как работает скрипт?
1) При каждом новом запуске скрипта создается таблица в БД.
2) Если запрос равен "exit" работа скрипта завершается, иначе запрос передается в функцию parse_requests() - это парсер который разбивает строку по "--" при правильной структуре запроса получается 1 команда (которая должна находится в словаре CLI)  и 3 аргумента(флага), если условие не выполняется то получаем вывод об ошибке.
3) Аргументы разбиваются на ключ и значение  и передаются в validator() - проврка значений на отсутсвие и необходимый тип данных, а также соответсвует ли аргумент переданной команде.
4) Если все данные прошли проверку, parse_requests() возвращает словарь. Пример: <b>{'command': 'deposit', 'client': 'John Jones', 'amount': 100, 'description': 'ATM Deposit'}</b>
5) Далее из этого словаря определяется команда для обращения к БД. И в метод класса Database предается полученный словарь.

## Prerequisites:
* python 3.10
* Git

## Установка и запуск:  
<pre>
$ git clone https://github.com/impuls64s/tz_NtPro.git
$ cd tz_NtPro
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt

<i>Запуск скрипта</i>
$ python scripts/bank.py

<i>Остановить скрипт</i>
> exit
</pre>
