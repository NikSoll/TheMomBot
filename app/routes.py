from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, Bot
from app.template_handler import get_template_path, copy_template, find_config_file, replace_in_file
import os

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    templates = [
        {'code': 'make', 'name': 'Запись на услуги', 'desc': 'Для салонов красоты'},
        {'code': 'shop', 'name': 'Интернет-магазин', 'desc': 'Продажа товаров'},
        {'code': 'quiz', 'name': 'Квиз-бот', 'desc': 'Тесты и викторины'},
        {'code': 'survey', 'name': 'Опросник', 'desc': 'Сбор обратной связи'},
        {'code': 'mailer', 'name': 'Рассыльщик', 'desc': 'Рассылка новостей'},
    ]
    return render_template('index.html', templates=templates)


@main_bp.route('/choose-template/<platform>')
def choose_template(platform):
    templates = [
        {'code': 'make', 'name': 'Запись на услуги', 'desc': 'Для салонов красоты'},
        {'code': 'shop', 'name': 'Интернет-магазин', 'desc': 'Продажа товаров'},
        {'code': 'quiz', 'name': 'Квиз-бот', 'desc': 'Тесты и викторины'},
        {'code': 'survey', 'name': 'Опросник', 'desc': 'Сбор обратной связи'},
        {'code': 'mailer', 'name': 'Рассыльщик', 'desc': 'Рассылка новостей'},
    ]
    return render_template('choose_template.html', platform=platform, templates=templates)


@main_bp.route('/choose-platform')
def choose_platform():
    return render_template('choose_platform.html')


@main_bp.route('/create/<platform>/<bot_type>')
def create_bot_form(platform, bot_type):
    if not platform or not bot_type:
        flash('Ошибка: не указана платформа или тип бота', 'danger')
        return redirect(url_for('main.choose_platform'))
    try:
        return render_template(f'create/{platform}/{bot_type}.html')
    except:
        flash(f'Шаблон create/{platform}/{bot_type}.html не найден', 'danger')
        return redirect(url_for('main.choose_template', platform=platform))


@main_bp.route('/create', methods=['GET','POST'])
def create_bot():
    #это бааазааа
    bot_token = ''
    vk_token = ''
    max_key = ''
    group_id = ''
    admin_id = '6496349641'
    shop_name = 'Салон красоты'
    address = 'г. Омск, ул. Масленникова, д. 45'
    phone = '+7 (905) 190-01-54'
    hours = 'Пн-Пт: 10:00-20:00, Сб-Вс: 11:00-18:00'
    masters = []
    available_times = []

    platform = request.form.get('platform')
    bot_type = request.form.get('bot_type')
    bot_name = request.form.get('bot_name')

    #тг
    if platform == 'tg':
        bot_token = request.form.get('bot_token')
        admin_id = request.form.get('admin_id', '6496349641')

        #для записи мастера
        masters = []
        names = request.form.getlist('master_name[]')
        emojis = request.form.getlist('master_emoji[]')

        for i, name in enumerate(names):
            if name.strip():
                masters.append({
                    'id': i + 1,
                    'name': name,
                    'emoji': emojis[i] if i < len(emojis) else '👤'
                })

        #все остальное
        shop_name = request.form.get('shop_name', 'Салон красоты')
        address = request.form.get('address', 'г. Омск, ул. Масленникова, д. 45')
        phone = request.form.get('phone', '+7 (905) 190-01-54')
        hours = request.form.get('hours', 'Пн-Пт: 10:00-20:00, Сб-Вс: 11:00-18:00')
        available_times = request.form.get('available_times', '10:00\n11:00\n12:00').split('\n')

    #вк
    elif platform == 'vk':
        vk_token = request.form.get('vk_token')
        group_id = request.form.get('group_id')
        admin_id = request.form.get('admin_id', '6496349641')

        #собираем мастеров
        masters = []
        names = request.form.getlist('master_name[]')
        emojis = request.form.getlist('master_emoji[]')

        for i, name in enumerate(names):
            if name.strip():
                masters.append({
                    'id': i + 1,
                    'name': name,
                    'emoji': emojis[i] if i < len(emojis) else '👤'
                })

        #каты и товары
        categories = request.form.get('categories', '').split('\n')
        products = request.form.get('products', '').split('\n')

        #для замены
        if bot_type == 'shop':
            # формируем список категорий
            cats_list = []
            for i, cat in enumerate(categories):
                if cat.strip():
                    cats_list.append({'id': i + 1, 'name': cat.strip()})
            #позже добавить в replacements не забыть

    #макс
    elif platform == 'max':
        max_key = request.form.get('max_key')
        bot_id = request.form.get('bot_id')
        admin_id = request.form.get('admin_id', '6496349641')
        webhook_url = request.form.get('webhook_url', '')
        secret_key = request.form.get('secret_key', '')

        #общ логика
        bot_token = max_key

        #make
        masters = []
        names = request.form.getlist('master_name[]')
        emojis = request.form.getlist('master_emoji[]')
        descs = request.form.getlist('master_desc[]')
        specialties = request.form.getlist('master_specialty[]')

        for i, name in enumerate(names):
            if name.strip():
                masters.append({
                    'id': i + 1,
                    'name': name,
                    'emoji': emojis[i] if i < len(emojis) else '👤',
                    'desc': descs[i] if i < len(descs) else '',
                    'specialty': specialties[i] if i < len(specialties) else ''
                })

        #услуги
        services = []
        service_names = request.form.getlist('service_name[]')
        service_prices = request.form.getlist('service_price[]')
        service_durations = request.form.getlist('service_duration[]')
        service_descs = request.form.getlist('service_desc[]')

        for i, name in enumerate(service_names):
            if name.strip():
                services.append({
                    'id': i + 1,
                    'name': name,
                    'price': service_prices[i] if i < len(service_prices) else 0,
                    'duration': service_durations[i] if i < len(service_durations) else 60,
                    'desc': service_descs[i] if i < len(service_descs) else ''
                })

        #shop
        categories = []
        cat_names = request.form.getlist('category_name[]')
        cat_emojis = request.form.getlist('category_emoji[]')

        for i, name in enumerate(cat_names):
            if name.strip():
                categories.append({
                    'id': i + 1,
                    'name': name,
                    'emoji': cat_emojis[i] if i < len(cat_emojis) else '📦'
                })

        #товары
        products = []
        prod_names = request.form.getlist('product_name[]')
        prod_prices = request.form.getlist('product_price[]')
        prod_cats = request.form.getlist('product_category[]')
        prod_descs = request.form.getlist('product_desc[]')
        prod_photos = request.form.getlist('product_photo[]')

        for i, name in enumerate(prod_names):
            if name.strip():
                products.append({
                    'id': i + 1,
                    'name': name,
                    'price': prod_prices[i] if i < len(prod_prices) else 0,
                    'category_id': prod_cats[i] if i < len(prod_cats) else 1,
                    'desc': prod_descs[i] if i < len(prod_descs) else '',
                    'photo': prod_photos[i] if i < len(prod_photos) else None
                })

        #quiz/survey
        questions = []
        q_texts = request.form.getlist('question_text[]')
        q_types = request.form.getlist('question_type[]')
        q_options = request.form.getlist('question_options[]')
        q_points = request.form.getlist('question_points[]')

        for i, text in enumerate(q_texts):
            if text.strip():
                questions.append({
                    'id': i + 1,
                    'text': text,
                    'type': q_types[i] if i < len(q_types) else 'text',
                    'options': q_options[i].split('\n') if i < len(q_options) else [],
                    'points': q_points[i] if i < len(q_points) else ''
                })

        #резы
        results = []
        r_types = request.form.getlist('result_type[]')
        r_texts = request.form.getlist('result_text[]')

        for i, r_type in enumerate(r_types):
            if r_type.strip():
                results.append({
                    'type': r_type,
                    'text': r_texts[i] if i < len(r_texts) else ''
                })

        #группы mailer
        groups = []
        group_names = request.form.getlist('group_name[]')

        for i, name in enumerate(group_names):
            if name.strip():
                groups.append({
                    'id': i + 1,
                    'name': name
                })

        #доп поля
        shop_name = request.form.get('shop_name', 'Мой магазин')
        address = request.form.get('address', '')
        phone = request.form.get('phone', '')
        available_times = request.form.get('available_times', '10:00\n11:00\n12:00').split('\n')
        booking_days = request.form.get('booking_days', 7)

        #сейв данных в БД или в config
        print(f"MAX бот: {bot_name}, тип: {bot_type}")

    #пока так потом как-нибудь поправлю
    user = User.query.first()
    if not user:
        user = User(email='test@example.com')
        db.session.add(user)
        db.session.commit()

    bot = Bot(
        user_id=user.id,
        name=bot_name,
        bot_type=bot_type,
        platform=platform,
        token=bot_token if platform == 'tg' else vk_token if platform == 'vk' else max_key
    )
    db.session.add(bot)
    db.session.commit()

    template_path = get_template_path(platform, bot_type)
    bot_path = f'bots/generated/{platform}_{bot.id}'
    os.makedirs('bots/generated', exist_ok=True)

    if template_path and copy_template(template_path, bot_path):
        config_file = find_config_file(bot_path)
        if config_file:
            #все
            replacements = {
                '"8574049417:AAHW-sdccf78WSer73GW3pPYXOstWqj6HSw"': f'"{bot_token}"',
                '"6496349641"': f'"{admin_id}"',
                'YOUR_BOT_TOKEN': bot_token,
                'YOUR_ADMIN_ID': admin_id,

                'Салон красоты': shop_name,
                'Мой магазин': shop_name,

                'г. Омск, ул. Масленникова, д. 45': address,
                '+7 (905) 190-01-54': phone,
                'Пн-Пт: 10:00-20:00, Сб-Вс: 11:00-18:00': hours,
            }

            #мастера
            if masters:
                import json
                replacements[
                    'MASTERS = [\n    {"id": 1, "name": "Анна", "emoji": "💅"},\n    {"id": 2, "name": "Мария", "emoji": "✨"},\n    {"id": 3, "name": "Ольга", "emoji": "🌟"},\n]'] = f'MASTERS = {json.dumps(masters, indent=4, ensure_ascii=False)}'

            #время
            if available_times:
                times_str = '[' + ', '.join(f'"{t.strip()}"' for t in available_times if t.strip()) + ']'
                replacements[
                    '["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]'] = times_str

            #вк
            if platform == 'vk':
                replacements['{{VK_TOKEN}}'] = vk_token
                replacements['{{GROUP_ID}}'] = group_id

            #замена и лог
            replace_in_file(config_file, replacements)
            flash(f'✅ Бот {bot_name} создан!', 'success')
        else:
            flash('⚠️ Бот создан, но конфиг не найден', 'warning')
    else:
        flash('❌ Ошибка: шаблон не найден', 'danger')

    return redirect(url_for('main.index'))


#все боты
@main_bp.route('/bots')
def list_bots():
    bots = Bot.query.all()
    return render_template('bots.html', bots=bots)