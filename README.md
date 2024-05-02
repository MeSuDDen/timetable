1. Скачать Python (у меня версия: 3.11.9)
2. Создать переменно окружение - **Python -m venv .env** или может так **python3 -m venv .env**;
3. Войти в переменное окружение - **.env/Scripts/activate**
4. Скачать необходимые зависимости:
   - **pip install flask**
   - **pip install flask_mail**
   - **pip install flask_migrate**
   - **pip install flask_sqlalchemy**
   - **pip install flask_wtf**
5. Запустить проект - **flask run --debug**
6. Возможно надо будет установить Tailwind (**npm install -D tailwindcss** + **npx tailwindcss init** + **npm install flowbite**) 
7. Для установки библиотек из пункта 6 нужно иметь на ПК скаченную nodejs (Первая ссылка в инете)


>Пояснение
> - В папке static находятся статические файлы, а также в папке static/uploads/.. находятся изображения которые мы загружаем. (Они если что автоматически не удаляются, так что их нужно подчищать если они не нужны)
> - В папке template находятся шаблоны html страниц.
> - В папке migration находятся миграции базы данных.
> - В папке app/... находятся файлы:
> - - config.py - конфигурация сервера
> - - app.db - это файл базы данных, он генерируется при создании бд с помощью "flask db init" + "flask db migrate -m 'Создание базы данных'" + "flask db init"
> - - models.py - содержит модели таблиц для базы данных
> - - routes.py - содержит маршрутизацию сервера и логику

