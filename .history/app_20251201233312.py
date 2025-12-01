"""
FlowPack - Бэкенд для отправки заявок в Telegram
"""

from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

# ============================================
# НАСТРОЙКИ TELEGRAM - ЗАМЕНИТЕ НА СВОИ!
# ============================================
# 1. Создайте бота: напишите @BotFather в Telegram, отправьте /newbot
# 2. Скопируйте токен бота сюда:
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8377802007:AAHn0zTCjtGvcQfnv-9UwfwcgQ6Lb07oMqI')

# 3. Узнайте свой chat_id: напишите боту @userinfobot или @getmyid_bot
# 4. Вставьте ваш chat_id сюда:
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '5594832715')
# ============================================


def send_telegram_message(message: str) -> bool:
    """Отправляет сообщение в Telegram"""
    if TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("⚠️  Telegram не настроен! Установите TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID")
        print(f"Сообщение которое должно было уйти:\n{message}")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False


@app.route('/')
def index():
    """Главная страница"""
    return send_from_directory('.', 'index.html')


@app.route('/api/contact', methods=['POST'])
def contact_form():
    """Обработка формы обратной связи"""
    data = request.get_json()
    
    name = data.get('name', 'Не указано')
    phone = data.get('phone', 'Не указан')
    email = data.get('email', 'Не указан')
    comment = data.get('comment', 'Нет комментария')
    
    now = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    message = f"""
📬 <b>Новая заявка с сайта!</b>

👤 <b>Имя:</b> {name}
📞 <b>Телефон:</b> {phone}
📧 <b>Email:</b> {email}
💬 <b>Комментарий:</b> {comment}

🕐 <i>{now}</i>
"""
    
    success = send_telegram_message(message)
    
    if success:
        return jsonify({'success': True, 'message': 'Заявка отправлена!'})
    else:
        # Даже если Telegram не настроен, говорим что всё ок (для тестирования)
        return jsonify({'success': True, 'message': 'Заявка принята!'})


@app.route('/api/callback', methods=['POST'])
def callback_form():
    """Обработка формы обратного звонка"""
    data = request.get_json()
    
    name = data.get('name', 'Не указано')
    phone = data.get('phone', 'Не указан')
    
    now = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    message = f"""
📞 <b>Запрос обратного звонка!</b>

👤 <b>Имя:</b> {name}
📞 <b>Телефон:</b> {phone}

🕐 <i>{now}</i>
"""
    
    success = send_telegram_message(message)
    
    return jsonify({'success': True, 'message': 'Мы вам перезвоним!'})


@app.route('/api/calculator', methods=['POST'])
def calculator_form():
    """Обработка заявки из калькулятора"""
    data = request.get_json()
    
    name = data.get('name', 'Не указано')
    phone = data.get('phone', 'Не указан')
    product = data.get('product', 'Не указан')
    quantity = data.get('quantity', 'Не указано')
    services = data.get('services', [])
    delivery = data.get('delivery', 'Не указана')
    total = data.get('total', '0')
    
    services_text = ', '.join(services) if services else 'Не выбраны'
    now = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    message = f"""
🧮 <b>Заявка из калькулятора!</b>

👤 <b>Имя:</b> {name}
📞 <b>Телефон:</b> {phone}

📦 <b>Товар:</b> {product}
🔢 <b>Количество:</b> {quantity} шт.
✅ <b>Услуги:</b> {services_text}
🚚 <b>Доставка:</b> {delivery}

💰 <b>Итого:</b> {total} ₽

🕐 <i>{now}</i>
"""
    
    success = send_telegram_message(message)
    
    return jsonify({'success': True, 'message': 'Заявка отправлена!'})


# Для статических файлов (CSS, JS, изображения)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)


if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════╗
║           🚀 FlowPack Server Started!                     ║
╠═══════════════════════════════════════════════════════════╣
║  Сайт доступен: http://localhost:5000                     ║
║                                                           ║
║  Для настройки Telegram:                                  ║
║  1. Создайте бота через @BotFather                        ║
║  2. Установите переменные окружения:                      ║
║     export TELEGRAM_BOT_TOKEN="ваш_токен"                 ║
║     export TELEGRAM_CHAT_ID="ваш_chat_id"                 ║
║                                                           ║
║  Или измените значения в app.py                           ║
╚═══════════════════════════════════════════════════════════╝
""")
    app.run(host='0.0.0.0', port=5000, debug=True)

