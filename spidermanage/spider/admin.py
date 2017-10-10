from django.contrib import admin
from models import Spider, DatabaseType, Message

class SpiderAdmin(admin.ModelAdmin):
    list_display = ('spider_name', 'spider_runing', 'spider_runfunction')


class DatabaseTypeAdmin(admin.ModelAdmin):
    list_display = ('DBname',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('content','action_time')


admin.site.register(Spider, SpiderAdmin)
admin.site.register(DatabaseType, DatabaseTypeAdmin)
admin.site.register(Message, MessageAdmin)

