from django.contrib import admin
from .models import UserQuery


@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'telegram_id', 'status', 'created_at')
    list_filter   = ('status', 'created_at')
    search_fields = ('username', 'first_name', 'query_text', 'telegram_id')
    readonly_fields = (
        'telegram_id', 'username', 'first_name',
        'query_text', 'bot_response', 'created_at'
    )
    fields = (
        'telegram_id', 'username', 'first_name',
        'query_text', 'bot_response',
        'admin_reply', 'status', 'created_at'
    )

    def save_model(self, request, obj, form, change):
        """Автоматически меняет статус когда администратор пишет ответ."""
        if obj.admin_reply and obj.status == 'support':
            obj.status = 'answered'
        super().save_model(request, obj, form, change)