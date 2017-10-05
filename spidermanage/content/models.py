#coding=utf-8
from django.db import models
from DjangoUeditor.models import UEditorField
import time



# 文章模型
class Article(models.Model):
    # 标题
    title = models.CharField(max_length=1000)
    # 文章id
    articel_id = models.FloatField(null=False,blank=False,default=time.time())
    # 作者
    author = models.CharField(max_length=1000)
    # 作品类型
    articel_type = models.ForeignKey('ArticelType')
    # 标签
    articel_tag = models.ManyToManyField('TagType')
    # 发布时间
    release_date = models.DateTimeField(auto_now_add=True,editable=True)
    # 修改时间
    update_time = models.DateTimeField(auto_now=True,null=True)
    # 文章正文
    content = UEditorField(height=300, width=1000, default=u'', blank=True, imagePath="uploads/blog/images/",
                           toolbars='besttome', filePath='uploads/blog/files/')
    # 说明
    mark = models.CharField(max_length=1000,default='no mark')
    # 摘要
    shortnote = models.CharField(max_length=1000,default='no shortnote')
    # 是否删除
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.title.encode('utf-8')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'


    # 文章类型模型
class ArticelType(models.Model):
    # 类型名称
    typename = models.CharField(max_length=50)
    # 逻辑删除
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.typename.encode('utf-8')

    class Meta:
        verbose_name = '文章类型'
        verbose_name_plural = '文章类型'



# 文章标签模型
class TagType(models.Model):
    # 标签名称
    tagname = models.CharField(max_length=50)
    # 文章
    articel = models.ManyToManyField('Article')
    # 逻辑删除
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.tagname.encode('utf-8')

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = '文章标签'



class Comment(models.Model):
    # 对应的文章id
    articel =  models.ForeignKey('Article')
    # 发布时间
    release_date = models.DateTimeField(auto_now_add=True, editable=True)
    # 逻辑删除
    isDelete = models.BooleanField(default=False)
    # 留言内容
    content = UEditorField(height=300, width=1000, default=u'', blank=True, imagePath="uploads/blog/images/",
                           toolbars='besttome', filePath='uploads/blog/files/')

    user = models.CharField(max_length=50)

    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural = '文章评论'


























