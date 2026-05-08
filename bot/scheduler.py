import os
import sys
import django
from datetime import timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_finder.settings')
django.setup()

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.utils import timezone
import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


def send_pending_reminders():
    """
    Запускается каждую минуту.
    Находит все активные напоминания у которых пришло время — отправляет.
    """
    from catalog.models import Reminder

    now = timezone.now()
    due = Reminder.objects.filter(active=True, send_at__lte=now)

    for reminder in due:
        try:
            bot.send_message(
                reminder.telegram_id,
                f'🔔 *Напоминание*\n\n{reminder.message}',
                parse_mode='Markdown',
            )
            print(f'[Scheduler] Отправлено напоминание → {reminder.telegram_id}')

            if reminder.repeat == 'daily':
                reminder.send_at = now + timedelta(days=1)
                reminder.save()
            elif reminder.repeat == 'weekly':
                reminder.send_at = now + timedelta(weeks=1)
                reminder.save()
            else:
                # Одноразовое — деактивируем
                reminder.active = False
                reminder.save()

        except Exception as e:
            print(f'[Scheduler] Ошибка отправки → {reminder.telegram_id}: {e}')


def send_pending_admin_replies():
    """
    Запускается каждые 10 секунд.
    Находит запросы где администратор написал ответ — отправляет в Telegram.
    """
    from catalog.models import UserQuery

    pending_replies = UserQuery.objects.filter(
        admin_reply__gt='',
        reply_sent=False,
    )

    for query in pending_replies:
        try:
            text = (
                f'📩 *Ответ от поддержки AstroBook*\n\n'
                f'Ваш вопрос: _{query.query_text}_\n\n'
                f'💬 Ответ: {query.admin_reply}'
            )
            bot.send_message(
                query.telegram_id,
                text,
                parse_mode='Markdown',
            )
            query.reply_sent = True
            query.save()
            print(f'[Scheduler] Ответ поддержки отправлен → {query.telegram_id}')

        except Exception as e:
            print(f'[Scheduler] Ошибка ответа поддержки → {query.telegram_id}: {e}')


def start_scheduler():
    """Запускает планировщик задач."""
    scheduler = BackgroundScheduler(timezone='Asia/Almaty')

    # Проверка напоминаний — каждую минуту
    scheduler.add_job(
        send_pending_reminders,
        trigger=IntervalTrigger(minutes=1),
        id='reminders',
        replace_existing=True,
    )

    # Проверка ответов поддержки — каждые 10 секунд
    scheduler.add_job(
        send_pending_admin_replies,
        trigger=IntervalTrigger(seconds=10),
        id='admin_replies',
        replace_existing=True,
    )

    scheduler.start()
    print('[Scheduler] ✅ Планировщик запущен')
    return scheduler