# API учета посещенных ссылок


## Для запуска проекта потребуются:
- Python >= 3.8, Redis >= 5.0.7, Docker >=20.10.7
- Склонировать проект и перейти в папку проекта
```bash
git clone https://github.com/dangerousmonk/FunBoxAPI
cd FunBoxAPI
```

## Запуск проекта через Docker
Проект можно запустить используя контейнеризацию. <br>
- Запустить сборку ```docker-compose``` командой ```docker-compose up``` <br>
находясь в корневой папке проекта

## Запуск проекта локально
- Активировать виртуальное окружение, или создать новый проект в PyCharm
```bash
python3 -m venv venv
source venv\bin\activate
```

- Установить зависимости из файла **requirements.txt**
 
```bash
pip install -r requirements.txt
``` 

-Запустить Redis-server(Linux или WSL):
```bash
redis-server
```

-Запустить проект:
```bash
python manage.py runserver
```

-Запустить тесты:
```bash
pytest
```




