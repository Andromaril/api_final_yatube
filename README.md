# api_final

Проект демонстрирует работу API с социльной сетью.

<h2>Как запустить проект:</h2>
Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/Andromaril/api_final_yatube.git

*Cоздать и активировать виртуальное окружение:*

1. python3 -m venv env
2. source env/bin/activate

*Установить зависимости из файла requirements.txt:*

1.python3 -m pip install --upgrade pip
2. pip install -r requirements.txt

*Выполнить миграции:*

python3 manage.py migrate

*Запустить проект:*

python3 manage.py runserver
