# 🏍️ Система записи на мото-тренировки

Веб-приложение на Django для управления тренировками, записи участников и интеграции с Telegram Mini App.

## 📌 Возможности

- Администрирование тренировок (темы, время, лимит участников)
- Запись участников на тренировки по темам и времени
- Автоматическое закрытие тренировок при достижении лимита
- Telegram-бот с мини-приложением для подачи заявки
- Уведомления в Telegram при открытии/закрытии тренировок
- Админка Django с возможностью просматривать заявки

---

## 🚀 Установка и запуск

### Нативный запуск

#### 1. Клонировать репозиторий

```bash
git clone https://github.com/vanche93/leehaaatch-trainy.git
cd leehaaatch-trainy
```

#### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

#### 3. Настроить `.env` или `settings.py`

Создайте файл `.env` или добавьте в `settings.py`:

```
MEDIA_ROOT='./uploads'
SECRET_KEY='secret-key'
DEBUG='false'
ALLOWED_HOSTS='your.host'
CSRF_TRUSTED_ORIGINS="https://your.host"
DATABASES_DIR='./db.sqlite3' 
TELEGRAM_BOT_TOKEN='bot_token'
TELEGRAM_CHAT_ID='chat_id'
TELEGRAM_MINIAPP_URL='https://t.me/your_bot/your_mini_app_url'
```

#### 4. Применить миграции и создать суперпользователя

```bash
python app/manage.py migrate
python app/manage.py createsuperuser
```

#### 5. Запустить сервер

```bash
python app/manage.py runserver
```

### Docker compose

#### 1. Клонировать репозиторий

```bash
git clone https://github.com/vanche93/leehaaatch-trainy.git
cd leehaaatch-trainy
```

#### 2. Настроить `.env`

Создайте файл `.env` или добавьте в `settings.py`:

```
MEDIA_ROOT='/uploads'
STATIC_ROOT='/static'
SECRET_KEY='secret-key'
DEBUG='false'
ALLOWED_HOSTS='your.host'
CSRF_TRUSTED_ORIGINS="https://your.host"
DATABASES_DIR='./db.sqlite3' 
TELEGRAM_BOT_TOKEN='bot_token'
TELEGRAM_CHAT_ID='chat_id'
TELEGRAM_MINIAPP_URL='https://t.me/your_bot/your_mini_app_url'
```

#### 3. Запустить

```bash
docker compose up --build
```

#### 4. Cоздать суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 💬 Telegram Mini App

- Бот отправляет кнопку пользователю, ведущую в web-app форму записи
- Форма загружается внутри Telegram (mini-app)
- Записи проверяются и при совпадении тем и времени от 4+ человек — тренировка закрывается
- Бот отправляет уведомление о закрытии/открытии

---

## 🔧 Основные модели

- `Training` — тренировка
- `TrainingTime` — варианты времени
- `TrainingTopic` — темы
- `TrainingReq` — заявка на тренировку
- `Student` — участник

---

## 🧠 Бизнес-логика

- Заявка содержит темы и время
- При 4 совпадающих заявках (тема + время) тренировка получает статус `full`
- В группу отправляется уведомление

---

## 📄 Лицензия

MIT License