# FlowPack — Сайт фулфилмент-компании

Современный сайт-визитка с отправкой заявок в Telegram.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
cd /home/user/site-ff
pip install -r requirements.txt
```

### 2. Настройка Telegram бота

1. Откройте Telegram и найдите **@BotFather**
2. Отправьте `/newbot` и следуйте инструкциям
3. Скопируйте полученный **токен бота**
4. Узнайте свой **chat_id** — напишите боту **@userinfobot** или **@getmyid_bot**

### 3. Запуск

**Способ 1: Через переменные окружения (рекомендуется)**

```bash
export TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
export TELEGRAM_CHAT_ID="987654321"
python app.py
```

**Способ 2: Напрямую в коде**

Откройте `app.py` и замените значения:
```python
TELEGRAM_BOT_TOKEN = 'ваш_токен_бота'
TELEGRAM_CHAT_ID = 'ваш_chat_id'
```

Затем запустите:
```bash
python app.py
```

### 4. Откройте в браузере

```
http://localhost:5000
```

---

## 🌐 Деплой на сервер

### Вариант 1: VPS с Ubuntu/Debian

```bash
# 1. Установите Python и pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 2. Загрузите файлы на сервер
scp -r /home/user/site-ff user@your-server:/var/www/

# 3. Создайте виртуальное окружение
cd /var/www/site-ff
python3 -m venv venv
source venv/bin/activate

# 4. Установите зависимости
pip install -r requirements.txt

# 5. Запустите через gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

### Вариант 2: Systemd сервис (автозапуск)

Создайте файл `/etc/systemd/system/flowpack.service`:

```ini
[Unit]
Description=FlowPack Website
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/site-ff
Environment="TELEGRAM_BOT_TOKEN=ваш_токен"
Environment="TELEGRAM_CHAT_ID=ваш_chat_id"
ExecStart=/var/www/site-ff/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Активируйте сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable flowpack
sudo systemctl start flowpack
```

### Вариант 3: Nginx + Gunicorn

Конфиг Nginx (`/etc/nginx/sites-available/flowpack`):

```nginx
server {
    listen 80;
    server_name your-domain.ru;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/flowpack /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 📁 Структура проекта

```
site-ff/
├── index.html          # Главная страница
├── app.py              # Python бэкенд (Flask)
├── requirements.txt    # Зависимости Python
└── README.md           # Эта документация
```

## 🔧 API Endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/` | Главная страница |
| POST | `/api/contact` | Форма обратной связи |
| POST | `/api/calculator` | Заявка из калькулятора |
| POST | `/api/callback` | Запрос обратного звонка |

## 📱 Формат сообщений в Telegram

При отправке формы вы получите красиво оформленное сообщение:

```
📬 Новая заявка с сайта!

👤 Имя: Иван Иванов
📞 Телефон: +7 (999) 123-45-67
📧 Email: ivan@mail.ru
💬 Комментарий: Хочу узнать про условия

🕐 01.12.2024 15:30
```

---

## ❓ Возможные проблемы

**Заявки не приходят в Telegram:**
- Проверьте правильность токена бота
- Убедитесь, что вы написали своему боту хотя бы одно сообщение
- Проверьте chat_id — он должен быть числом

**Ошибка CORS:**
- Убедитесь, что сайт открыт через `http://localhost:5000`, а не как файл

**Порт 5000 занят:**
- Измените порт в `app.py`: `app.run(port=8080)`

