from django.db import models


class UserQuery(models.Model):
    """Хранит каждый запрос пользователя из Telegram-бота."""

    STATUS_CHOICES = [
        ('answered', 'Отвечено'),
        ('pending', 'Ожидает ответа'),
        ('support', 'Передано в поддержку'),
    ]

    telegram_id    = models.BigIntegerField(verbose_name='Telegram ID')
    username       = models.CharField(max_length=150, blank=True, verbose_name='Username')
    first_name     = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    query_text     = models.TextField(verbose_name='Запрос пользователя')
    bot_response   = models.TextField(blank=True, verbose_name='Ответ бота')
    admin_reply    = models.TextField(blank=True, verbose_name='Ответ поддержки')
    status         = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='answered',
        verbose_name='Статус'
    )
    created_at     = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')

    class Meta:
        verbose_name        = 'Запрос пользователя'
        verbose_name_plural = 'Запросы пользователей'
        ordering            = ['-created_at']

    def __str__(self):
        name = self.username or self.first_name or str(self.telegram_id)
        return f'{name} — {self.query_text[:50]}'