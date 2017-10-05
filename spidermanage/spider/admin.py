from django.contrib import admin
from models import Spider, DatabaseType

class SpiderAdmin(admin.ModelAdmin):
    list_display = ('spider_name', 'spider_runing', 'spider_runfunction')


class DatabaseTypeAdmin(admin.ModelAdmin):
    list_display = ('DBname',)


admin.site.register(Spider, SpiderAdmin)
admin.site.register(DatabaseType, DatabaseTypeAdmin)

