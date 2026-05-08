from django.contrib import admin
from django.utils.html import format_html
from .models import UserQuery, Notification, Reminder


@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display   = ('display_name', 'short_query', 'status_badge', 'reply_sent', 'created_at')
    list_filter    = ('status', 'reply_sent', 'created_at')
    search_fields  = ('username', 'first_name', 'query_text', 'telegram_id')
    readonly_fields = (
        'telegram_id', 'username', 'first_name',
        'query_text', 'bot_response', 'reply_sent', 'created_at'
    )
    fields = (
        'telegram_id', 'username', 'first_name',
        'query_text', 'bot_response',
        'admin_reply', 'status', 'reply_sent', 'created_at'
    )

    def short_query(self, obj):
        return obj.query_text[:60] + '...' if len(obj.query_text) > 60 else obj.query_text
    short_query.short_description = 'Запрос'

    def status_badge(self, obj):
        colors = {
            'answered': '#27ae60',
            'pending':  '#f39c12',
            'support':  '#e74c3c',
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;'
            'border-radius:12px;font-size:12px">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and obj.status == 'support':
            obj.status = 'answered'
        super().save_model(request, obj, form, change)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ('title', 'sent', 'sent_count', 'created_at')
    readonly_fields = ('sent', 'sent_count', 'created_at')


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'send_at', 'repeat', 'active', 'created_at')
    list_filter   = ('repeat', 'active')
    search_fields = ('username', 'telegram_id', 'message')