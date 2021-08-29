# API учета посещенных ссылок

## Запуск проекта локально
- Склонировать проект и перейти в папку проекта

```bash
git clone https://github.com/dangerousmonk/FunBoxAPI
cd FunBoxAPI
```
- Установить Python >= 3.8 и Redis в случае если они не установлены
- Активировать виртуальное окружение, или создать новый проект в PyCharm

```bash
python3 -m venv venv
source venv\bin\activate
```

- Установить зависимости из файла **requirements.txt**
 
```bash
pip install -r requirements.txt
``` 

-Запустить Redis-server(Linux bash):
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




