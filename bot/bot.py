import os
import sys
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
    text = message.text.strip()

    if text in (BTN_HELP, '/help'):
        return handle_help(message)
    if text in (BTN_TOPICS, '/topics'):
        return handle_topics(message)

    topic = find_topic(text)
    if topic:
        reply(message, format_book_list(topic))
        return

    topics = ', '.join(BOOKS_CATALOG.keys())
    reply(message, (
        f'Не нашёл книги по запросу: *{text}*\n\n'
        'Запрос сохранён и передан в поддержку.\n\n'
        f'_Попробуй одну из тем:_ {topics}'
    ), status='support')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print('AstroBook started...')
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
