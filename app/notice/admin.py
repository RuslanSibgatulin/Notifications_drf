from django.contrib import admin

from .models import Client, Mailing, Message


@admin.register(Client)
class NoticeClientAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('phone', 'tag', 'tz')

    # Поиск по полям
    search_fields = ('phone', )

    # Фильтрация в списке
    list_filter = ('tag', 'tz')


@admin.register(Mailing)
class NoticeMailingAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('start_at', 'stop_at', 'tag')

    # Поиск по полям
    search_fields = ('message', 'tag')

    # Фильтрация в списке
    list_filter = ('start_at', 'stop_at')


@admin.register(Message)
class NoticeMessageAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    # list_display = (...)

    # Поиск по полям
    search_fields = ('id', 'name', 'description', )
