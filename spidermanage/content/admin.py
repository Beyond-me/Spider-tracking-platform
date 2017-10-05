from django.contrib import admin
from content.models import Article,ArticelType,TagType,Comment

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','release_date')

class ArticelTypeAdmin(admin.ModelAdmin):
    list_display = ('typename','isDelete')

class TagTypeAdmin(admin.ModelAdmin):
    list_display = ('tagname','isDelete')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('articel','release_date')





admin.site.register(Article,ArticleAdmin)
admin.site.register(ArticelType,ArticelTypeAdmin)
admin.site.register(TagType,TagTypeAdmin)
admin.site.register(Comment,CommentAdmin)