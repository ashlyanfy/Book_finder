import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import django
import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# ── Настройка Django до первого импорта моделей ──────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_finder.settings')
django.setup()

from catalog.models import UserQuery                                  # noqa: E402
from books_data import BOOKS_CATALOG, find_topic, format_book_list    # noqa: E402

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError('Переменная BOT_TOKEN не найдена в .env файле!')

bot = telebot.TeleBot(BOT_TOKEN)

BTN_HELP   = 'Помощь'
BTN_TOPICS = 'Все темы'


def save_query(message: Message, response: str, status: str = 'answered') -> None:
    UserQuery.objects.create(
        telegram_id=message.from_user.id,
        username=message.from_user.username or '',
        first_name=message.from_user.first_name or '',
        query_text=message.text or '',
        bot_response=response,
        status=status,
    )


def topics_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[KeyboardButton(t.capitalize()) for t in BOOKS_CATALOG])
    markup.add(KeyboardButton(BTN_HELP), KeyboardButton(BTN_TOPICS))
    return markup


def reply(message: Message, text: str, status: str = 'answered') -> None:
    bot.send_message(
        message.chat.id, text,
        parse_mode='Markdown',
        disable_web_page_preview=True,
        reply_markup=topics_keyboard(),
    )
    save_query(message, text, status)


@bot.message_handler(commands=['start'])
def handle_start(message: Message) -> None:
    name = message.from_user.first_name or 'читатель'
    reply(message, (
        f'Привет, *{name}*!\n\n'
        'Я — *AstroBook*. Помогу подобрать книги по любой теме.\n\n'
        'Просто напиши тему или выбери её на клавиатуре ниже.\n\n'
        '_Например: астрофизика, физика, история, психология…_'
    ))


@bot.message_handler(commands=['help'])
def handle_help(message: Message) -> None:
    topics = ', '.join(BOOKS_CATALOG.keys())
    reply(message, (
        '*Помощь*\n\n'
        'Напиши тему — пришлю подборку книг с описаниями и ссылками.\n\n'
        f'*Доступные темы:* {topics}\n\n'
        'Если темы нет — твой запрос сохранится и попадёт в поддержку.'
    ))


@bot.message_handler(commands=['topics'])
def handle_topics(message: Message) -> None:
    lines = ['*Все доступные темы:*\n']
    for topic, books in BOOKS_CATALOG.items():
        lines.append(f'• {topic.capitalize()} — {len(books)} книг')
    reply(message, '\n'.join(lines))


@bot.message_handler(content_types=['text'])
def handle_text(message: Message) -> None:
    # Обработка пустого ввода
    if not message.text or not message.text.strip():
        bot.send_message(
            message.chat.id,
            '⚠️ Пожалуйста, напиши название темы.',
            reply_markup=build_topics_inline()
        )
        return

    topic = find_topic(message.text)
    if topic:
        book_list = format_book_list(topic)
        bot.send_message(
            message.chat.id, book_list,
            parse_mode='Markdown',
            disable_web_page_preview=True,
            reply_markup=build_back_button(),
        )
        save_query(message, book_list)
    else:
        response = (
            f'🤔 Не нашёл книги по запросу: *{message.text}*\n\n'
            '📩 Вопрос передан в поддержку — скоро ответим!\n\n'
            '👇 Попробуй выбрать тему:'
        )
        bot.send_message(
            message.chat.id, response,
            parse_mode='Markdown',
            reply_markup=build_topics_inline(),
        )
        save_query(message, response, status='support')


class _HealthHandler(BaseHTTPRequestHandler):
    """Минимальный health-endpoint — нужен Render'у, чтобы не убить сервис."""

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'ok')

    def log_message(self, *_):
        pass


def _start_health_server():
    port = int(os.getenv('PORT', '8080'))
    HTTPServer(('0.0.0.0', port), _HealthHandler).serve_forever()


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    threading.Thread(target=_start_health_server, daemon=True).start()
    print('AstroBook started...')
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
