#coding=utf-8

from django.db import models
from DjangoUeditor.models import UEditorField


# 项目模型
class TProject(models.Model):
    # 项目名称
    project_name = models.CharField(max_length=100)
    # 项目标签
    project_tagname = models.ManyToManyField('ProjectTagType',blank=True)
    # 项目类型
    project_type = models.ForeignKey('ProjectType')
    # 项目链接
    project_url = models.CharField(max_length=200)
    # 项目描述
    project_desc = UEditorField(height=300, width=1000, default=u'', blank=True, imagePath="uploads/blog/images/",
                           toolbars='besttome', filePath='uploads/blog/files/')
    # 项目说明
    project_mark = models.CharField(max_length=100,default='no mark')
    # 发布时间
    release_date = models.DateTimeField(auto_now_add=True,editable=True)
    # 修改时间
    update_time = models.DateTimeField(auto_now=True,null=True)
    # 描述
    project_shortnote = models.CharField(max_length=200)
    # 是否删除
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.project_name.encode('utf-8')

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


# 项目标签模型
class ProjectTagType(models.Model):
    # 标签名称
    tagname = models.CharField(max_length=50)
    # 项目
    project = models.ManyToManyField('TProject',blank=True)
    # 逻辑删除
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.tagname.encode('utf-8')

    class Meta:
        verbose_name = '项目标签'
        verbose_name_plural = '项目标签'


# 项目类型模型
class ProjectType(models.Model):
    # 类型名称
    typename = models.CharField(max_length=50)
    # 逻辑删除
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.typename.encode('utf-8')

    class Meta:
        verbose_name = '项目类型'
        verbose_name_plural = '项目类型'


# 项目评论模型
class Comment(models.Model):
    # 对应的文章id
    project =  models.ForeignKey('TProject')
    # 发布时间
    release_date = models.DateTimeField(auto_now_add=True, editable=True)
    # 逻辑删除
    isDelete = models.BooleanField(default=False)
    # 留言内容
    content = UEditorField(height=300, width=1000, default=u'', blank=True, imagePath="uploads/blog/images/",
                           toolbars='besttome', filePath='uploads/blog/files/')
    # 留言用户
    user = models.CharField(max_length=50)

    def __str__(self):
        return self.content.encode('utf-8')

    class Meta:
        verbose_name = '项目评论'
        verbose_name_plural = '项目评论'










