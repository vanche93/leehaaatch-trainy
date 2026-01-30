import requests
import json
from django.conf import settings
import re


class Telegram:

    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def escape_md(self, text):
        escape_chars = r"_*`["
        return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

    def send_open_message(self, training):
        open_message = (
            f"✅ *Открыта запись на тренировку!*\n\n"
            + (f"📌 *Название:* {training.name}\n" if training.name else '')
            + f"📅 *Дата:* {training.date.strftime('%d.%m.%Y')}\n"
            + f"📍 *Место:* [{training.place.name}{", " + training.place.address if training.place.address else ''}]({training.place.yandex_maps_url()})\n"
            + f"📚 *Темы:*\n"
            + f"{chr(10).join([f'  • {t.name}' for t in training.topics.all()])}\n"
            + f"🕒 *Время:*\n"
            + f"{chr(10).join([f'  • {t}' for t in training.training_times.all()])}"
        )
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "Записатся на тренировку",
                        "url": settings.TELEGRAM_MINIAPP_URL + "?startapp=" + str(training.id),
                    }
                ]
            ]
        }
        data = {
            "chat_id": self.chat_id,
            "text": open_message,
            "parse_mode": "Markdown",
            "reply_markup": json.dumps(keyboard),
        }
        try:
            requests.post(self.url, data=data).raise_for_status()
        except Exception as e:
            print(f"Ошибка при отправке Telegram-сообщения: {e}")

    def send_close_message(self, training):
        close_message = (
            f"✅ *Тренировка собрана!*\n\n"
            + (f"📌 *Название:* {training.name}\n" if training.name else '')
            + f"📅 *Дата:* {training.date.strftime('%d.%m.%Y')}\n"
            + f"📍 *Место:* [{training.place.name}{", " + training.place.address if training.place.address else ''}]({training.place.yandex_maps_url()})\n"
            + f"📚 *Тема:* {training.final_topic}\n"
            + f"🕒 *Время:* {training.final_time}\n\n"
            + f"👥 *Участники:*\n"
            + f"{chr(10).join([f'  • @{self.escape_md(p.tg_name)}' for p in training.participants.all()])}"
        )
        data = {
            "chat_id": self.chat_id,
            "text": close_message,
            "parse_mode": "Markdown",
        }
        try:
            requests.post(self.url, data=data).raise_for_status()
        except Exception as e:
            print(f"Ошибка при отправке Telegram-сообщения: {e}")

    def send_close_message_participants(self, training):
        close_message = (
            f"✅ *Вы записаны на тренировку!*\n\n"
            + (f"📌 *Название:* {training.name}\n" if training.name else '')
            + f"📅 *Дата:* {training.date.strftime('%d.%m.%Y')}\n"
            + f"📍 *Место:* [{training.place.name}{", " + training.place.address if training.place.address else ''}]({training.place.yandex_maps_url()})\n"
            + f"📚 *Тема:* {training.final_topic}\n"
            + f"🕒 *Время:* {training.final_time}\n\n"
        )
        for participant in training.participants.all():
            data = {
                "chat_id": participant.tg_id,
                "text": close_message,
                "parse_mode": "Markdown",
            }
            try:
                requests.post(self.url, data=data).raise_for_status()
            except Exception as e:
                print(f"Ошибка при отправке Telegram-сообщения: {e}")

telegram = Telegram()
