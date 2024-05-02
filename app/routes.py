from flask import current_app, render_template_string, render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Course
from app.models import Group
from app.models import Image
from flask_mail import Mail, Message
import os
import uuid
from werkzeug.utils import secure_filename
from flask import jsonify
from flask import send_from_directory


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'rusokoro2002@gmail.com'  # Замените на ваш адрес электронной почты
app.config['MAIL_PASSWORD'] = 'ypur ojln ksci xzfv'         # Замените на ваш пароль от электронной почты

# Инициализация Flask-Mail
mail = Mail(app)

@app.route('/select_course', methods=['GET'])
def select_course():
    courses = Course.query.all()  # Получить список всех курсов из базы данных
    return render_template('select_course.html', courses=courses)

@app.route('/show_database')
def show_database():
    # Получаем все курсы
    courses = Course.query.all()

    # Получаем все группы
    groups = Group.query.all()

    # Получаем все изображения
    images = Image.query.all()

    # Выводим данные
    return render_template('show_database.html', courses=courses, groups=groups, images=images)

@app.route('/get_image')
def get_image():
    course_id = request.args.get('course_id')
    group_id = request.args.get('group_id')
    image = Image.query.filter_by(course_id=course_id, group_id=group_id).first()
    if image:
        return jsonify({'filename': image.filename})
    else:
        return jsonify({'filename': None})


@app.route('/dashboard', methods=['GET'])
def admin_panel():
    courses = Course.query.all()
    groups = Group.query.all()
    return render_template('admin.html', courses=courses, groups=groups)

@app.route('/create_course', methods=['POST'])
def create_course():
    course_name = request.form.get('course_name')
    course = Course(name=course_name)
    db.session.add(course)
    db.session.commit()
    flash('Course created successfully', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/create_group', methods=['POST'])
def create_group():
    group_name = request.form.get('group_name')
    course_id = request.form.get('course_id')
    group = Group(name=group_name, course_id=course_id)
    db.session.add(group)
    db.session.commit()
    flash('Group created successfully', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/upload_timetable', methods=['POST'])
def upload_timetable():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('admin_panel'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('admin_panel'))

    filename = str(uuid.uuid4()) + secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    group_id = request.form.get('group_id')
    course_id = request.form.get('course_id')  # Получаем course_id из запроса POST

    # Теперь можно сохранить изображение с указанием как group_id, так и course_id
    image = Image(filename=filename, group_id=group_id, course_id=course_id)
    db.session.add(image)
    db.session.commit()

    flash('Image uploaded successfully', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/get_groups')
def get_groups():
    course_id = request.args.get('course_id')
    groups = Group.query.filter_by(course_id=course_id).all()
    groups_data = [{'id': group.id, 'name': group.name} for group in groups]
    return jsonify(groups_data)


# Функция для удаления всех данных из базы данных

# def delete_all_records():
#     with app.app_context():
#         try:
#             # Удаление всех изображений
#             Image.query.delete()
#
#             # Удаление всех групп
#             Group.query.delete()
#
#             # Удаление всех курсов
#             Course.query.delete()
#
#             # Сохранение изменений в базе данных
#             db.session.commit()
#
#             print("All records have been deleted successfully.")
#         except Exception as e:
#             # Если произошла ошибка, откатываем транзакцию и выводим сообщение об ошибке
#             db.session.rollback()
#             print(f"An error occurred: {str(e)}")

# Вызов функции для удаления всех записей (Если нужно удалить, раскомментируй)
# delete_all_records()



@app.route('/send_image_email', methods=['POST'])
def send_image_email():
    # Получаем course_id и group_id из формы
    course_id = request.form.get('course_id')
    group_id = request.form.get('group_id')

    # Получаем изображение из базы данных
    image = Image.query.filter_by(course_id=course_id, group_id=group_id).first()
    if image:
        # Отправляем изображение по почте
        send_email(image.filename)
        flash('Image sent successfully', 'success')
    else:
        flash('Image not found', 'error')

    return redirect(url_for('select_course'))

def send_email(image_filename):
    # Создаем абсолютный URL для изображения
    image_path = os.path.join(current_app.root_path, '..', 'static', 'uploads', image_filename)
    image_url = url_for('static', filename='uploads/' + image_filename, _external=True)

    # Создаем сообщение
    sender = 'rusokoro2002@gmail.com'  # Замените на ваш адрес электронной почты
    recipients = ['rusokoro2002@gmail.com']  # Замените адрес получателя или оставьте пустым для отправки себе
    subject = 'Image from Admin Panel'

    # Создаем HTML-шаблон для тела сообщения
    html_body = """
    <p>Here is the image you requested:</p>
    <p><img src="{}" alt="Image"></p>
    """.format(image_url)

    # Прикрепляем изображение в тело письма
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = render_template_string(html_body)

    # Прикрепляем изображение как вложение
    with current_app.open_resource(image_path) as fp:
        msg.attach(image_filename, 'image/*', fp.read())

    # Отправляем сообщение
    mail.send(msg)
