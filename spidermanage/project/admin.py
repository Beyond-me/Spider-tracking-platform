from django.contrib import admin

from django.contrib import admin
from project.models import TProject,ProjectType,ProjectTagType,Comment

# Register your models here.

class TProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name','project_type')

class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('typename','isDelete')

class ProjectTagTypeAdmin(admin.ModelAdmin):
    list_display = ('tagname','isDelete')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('project','content')



admin.site.register(TProject,TProjectAdmin)
admin.site.register(ProjectType,ProjectTypeAdmin)
admin.site.register(ProjectTagType,ProjectTagTypeAdmin)
admin.site.register(Comment,CommentAdmin)
