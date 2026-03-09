import os
import shutil
from flask import(
    Flask, render_template,
    request, redirect,
    url_for, flash
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from setuptools.command.setopt import config_file
from sqlalchemy.orm import backref

import config

#создаем прилож и бд
app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)

#создаем папки
os.makedirs(app.config['BOTS_DIR'], exist_ok=True)

#одели
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    bot_type = db.Column(db.String(20))
    platform = db.Column(db.String(10), default='tg')
    token = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='bots')

#создание бд
with app.app_context():
    db.create_all()
    print("БД создана!!!")

#мфршруты
@app.route('/')
def index():
    templates = [
        {'code': 'make', 'name': 'Запись на услуги', 'desc': 'Для салонов красоты, парикмахерских и т.д.'},
        {'code': 'shop', 'name': 'Интернет-магазин', 'desc': 'Продажа товаров через бота'},
        {'code': 'quiz', 'name': 'Квиз-бот', 'desc': 'Тесты и викторины'},
        {'code': 'survey', 'name': 'Опросник', 'desc': 'Сбор обратной связи'},
        {'code': 'mailer', 'name': 'Рассыльщик-бот', 'desc': 'Рассылка новостей'},
    ]
    return render_template('index.html', templates=templates)


@app.route('/create', methods=['GET', 'POST'])
def create_bot():
    selected_type = request.args.get('type', 'make')
    selected_platform = request.args.get('platform', 'tg')

    if request.method == 'POST':
        platform = request.form.get('platform')
        bot_type = request.form.get('bot_type')
        bot_name = request.form.get('bot_name')
        bot_token = request.form.get('bot_token')
        group_id = request.form.get('group_id', '')  # для ВК

        user = User.query.first()
        if not user:
            user = User(email='test@example.com')
            db.session.add(user)
            db.session.commit()

        bot = Bot(
            user_id=user.id,
            name=bot_name,
            bot_type=bot_type,
            token=bot_token,
            platform=platform
        )
        db.session.add(bot)
        db.session.commit()

        template_path = f'templates/{platform}/{bot_type}'
        bot_path = f'bots/{platform}_{bot.id}'

        if os.path.exists(template_path):
            shutil.copytree(template_path, bot_path)

            config_file = os.path.join(bot_path, 'config.py')
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                if platform == 'tg':
                    content = content.replace('YOUR_BOT_TOKEN', bot_token)
                elif platform == 'vk':
                    content = content.replace('{{VK_TOKEN}}', bot_token)
                    content = content.replace('{{GROUP_ID}}', group_id)

                with open(config_file, 'w', encoding='utf-8') as f:
                    f.write(content)

            flash(f'Бот создан! Платформа: {platform}', 'success')
        else:
            flash(f'Шаблон {platform}/{bot_type} не найден', 'danger')

        return redirect(url_for('index'))

    return render_template('create.html', selected_type=selected_type, selected_platform=selected_platform)


@app.route('/bots')
def list_bots():
    bots = Bot.query.all()
    return render_template('bots.html', bots=bots)

if __name__ == '__main__':
    app.run(debug=True)