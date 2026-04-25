import os
import sys
import django
import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

# ── Настройка Django до первого импорта моделей ──────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_finder.settings')
django.setup()

from catalog.models import UserQuery          # noqa: E402  (после django.setup)
from books_data import (                      # noqa: E402
    BOOKS_CATALOG,
    find_topic,
    format_book_list,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError('Переменная BOT_TOKEN не найдена в .env файле!')

bot = telebot.TeleBot(BOT_TOKEN)

# ── Вспомогательные функции ───────────────────────────────────────────────────

def save_query(message: Message, bot_response: str, status: str = 'answered') -> None:
    """Сохраняет запрос пользователя и ответ бота в базу данных."""
    UserQuery.objects.create(
        telegram_id=message.from_user.id,
        username=message.from_user.username or '',
        first_name=message.from_user.first_name or '',
        query_text=message.text or '',
        bot_response=bot_response,
        status=status,
    )


def build_topics_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру со всеми доступными темами."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [KeyboardButton(topic.capitalize()) for topic in BOOKS_CATALOG]
    markup.add(*buttons)
    markup.add(KeyboardButton('❓ Помощь'), KeyboardButton('📋 Все темы'))
    return markup


# ── Обработчики команд ────────────────────────────────────────────────────────

@bot.message_handler(commands=['start'])
def handle_start(message: Message) -> None:
    name = message.from_user.first_name or 'читатель'
    text = (
        f'👋 Привет, *{name}*!\n\n'
        '📚 Я — *Book Finder Bot*.\n'
        'Помогу подобрать книги по любой теме.\n\n'
        '➡️ Просто напиши тему, которая тебя интересует, '
        'или выбери из кнопок ниже.\n\n'
        '*Пример:* астрофизика, физика, история, психология…'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown',
                     reply_markup=build_topics_keyboard())
    save_query(message, text)


@bot.message_handler(commands=['help'])
def handle_help(message: Message) -> None:
    topics = ', '.join(BOOKS_CATALOG.keys())
    text = (
        '🆘 *Помощь*\n\n'
        'Напиши название темы и я пришлю подборку книг с описаниями и ссылками.\n\n'
        f'📌 *Доступные темы:*\n{topics}\n\n'
        'Если не нашёл нужную тему — напиши запрос свободным текстом, '
        'и я передам его в поддержку.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown',
                     reply_markup=build_topics_keyboard())
    save_query(message, text)


@bot.message_handler(commands=['topics'])
def handle_topics(message: Message) -> None:
    lines = ['📋 *Все доступные темы:*\n']
    for topic in BOOKS_CATALOG:
        count = len(BOOKS_CATALOG[topic])
        lines.append(f'• {topic.capitalize()} — {count} книги')
    text = '\n'.join(lines)
    bot.send_message(message.chat.id, text, parse_mode='Markdown',
                     reply_markup=build_topics_keyboard())
    save_query(message, text)


# ── Обработчик текстовых сообщений ───────────────────────────────────────────

@bot.message_handler(content_types=['text'])
def handle_text(message: Message) -> None:
    user_text = message.text.strip()

    # Обработка кнопок меню
    if user_text in ('❓ Помощь', '/help'):
        return handle_help(message)
    if user_text in ('📋 Все темы', '/topics'):
        return handle_topics(message)

    # Поиск темы в сообщении пользователя
    topic = find_topic(user_text)

    if topic:
        book_list = format_book_list(topic)
        bot.send_message(
            message.chat.id,
            book_list,
            parse_mode='Markdown',
            disable_web_page_preview=True,
            reply_markup=build_topics_keyboard(),
        )
        save_query(message, book_list)
    else:
        # Тема не найдена — передаём запрос в поддержку
        response = (
            '🤔 Не нашёл книги по запросу: *{query}*\n\n'
            'Я сохранил твой вопрос и передал его в поддержку.\n'
            'Скоро получишь ответ! 📩\n\n'
            '💡 Попробуй одну из доступных тем:\n'
            '{topics}'
        ).format(
            query=user_text,
            topics=', '.join(BOOKS_CATALOG.keys()),
        )
        bot.send_message(message.chat.id, response, parse_mode='Markdown',
                         reply_markup=build_topics_keyboard())
        save_query(message, response, status='support')


# ── Запуск бота ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print('Book Finder Bot zapuschen...')
    bot.infinity_polling(timeout=10, long_polling_timeout=5)