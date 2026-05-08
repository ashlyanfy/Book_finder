from django.db import models


class UserQuery(models.Model):
    STATUS_CHOICES = [
        ('answered', 'Отвечено'),
        ('pending',  'Ожидает ответа'),
        ('support',  'Передано в поддержку'),
    ]

    telegram_id  = models.BigIntegerField(verbose_name='Telegram ID')
    username     = models.CharField(max_length=150, blank=True, verbose_name='Username')
    first_name   = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    query_text   = models.TextField(verbose_name='Запрос')
    bot_response = models.TextField(blank=True, verbose_name='Ответ бота')
    admin_reply  = models.TextField(blank=True, verbose_name='Ответ поддержки')
    reply_sent   = models.BooleanField(default=False, verbose_name='Ответ отправлен в Telegram')
    status       = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='answered', verbose_name='Статус'
    )
    created_at   = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name        = 'Запрос'
        verbose_name_plural = 'Запросы пользователей'
        ordering            = ['-created_at']

    def __str__(self):
        name = self.username or self.first_name or str(self.telegram_id)
        return f'{name} — {self.query_text[:50]}'

    @property
    def display_name(self):
        return self.username or self.first_name or f'ID:{self.telegram_id}'


class Notification(models.Model):
    """Массовые уведомления от администратора."""
    title      = models.CharField(max_length=200, verbose_name='Заголовок')
    message    = models.TextField(verbose_name='Текст уведомления')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    sent       = models.BooleanField(default=False, verbose_name='Отправлено')
    sent_count = models.IntegerField(default=0, verbose_name='Отправлено пользователям')

    class Meta:
        verbose_name        = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering            = ['-created_at']

    def __str__(self):
        return self.title


class Reminder(models.Model):
    """Напоминания пользователям по расписанию."""
    REPEAT_CHOICES = [
        ('once',    'Один раз'),
        ('daily',   'Каждый день'),
        ('weekly',  'Каждую неделю'),
    ]

    telegram_id = models.BigIntegerField(verbose_name='Telegram ID')
    username    = models.CharField(max_length=150, blank=True, verbose_name='Username')
    message     = models.TextField(verbose_name='Текст напоминания')
    send_at     = models.DateTimeField(verbose_name='Время отправки')
    repeat      = models.CharField(
        max_length=10, choices=REPEAT_CHOICES,
        default='once', verbose_name='Повтор'
    )
    active      = models.BooleanField(default=True, verbose_name='Активно')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name        = 'Напоминание'
        verbose_name_plural = 'Напоминания'
        ordering            = ['send_at']

    def __str__(self):
        name = self.username or str(self.telegram_id)
        return f'{name} — {self.message[:40]} ({self.get_repeat_display()})'