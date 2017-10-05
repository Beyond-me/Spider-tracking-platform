#coding=utf-8
from django.db import models


class Spider(models.Model):
    # 爬虫名称
    spider_name = models.CharField(max_length=50)
    # 爬虫的内容
    spider_content = models.CharField(max_length=200, default='暂无描述')
    # 爬虫目标网站
    spider_url = models.CharField(max_length=200, default='url')
    # 总请求次数
    spider_request_count = models.IntegerField(default=0)
    # 总下载次数
    spider_download_count = models.IntegerField(default=0)
    # 总储存的信息条数
    spider_info_count = models.IntegerField(default=0)
    # 报错次数
    spider_error_count = models.IntegerField(default=0)
    # 储存信息的数据库类型
    database_type = models.ForeignKey('DatabaseType', null=True, blank=True)
    # 储存信息的数据库库名称
    database_name = models.CharField(max_length=50, null=True, default='no info')
    # 储存信息的数据表名称
    database_sheetname = models.CharField(max_length=50, null=True, default='no info')
    # 爬虫运行状态
    spider_runing = models.BooleanField(default=False)
    # 爬虫启动函数
    spider_runfunction= models.CharField(max_length=50, null=True, default='no info')
    # 爬虫启动参数
    spider_runavg= models.CharField(max_length=100, null=True, default='no info')
    # 爬虫备注
    spider_mark = models.CharField(max_length=200, default='no mark')
    # 图片
    spider_pic = models.ImageField(null=True,blank=True)
    # 爬虫　逻辑删除
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.spider_name.encode('utf-8')

    class Meta:
        verbose_name = '爬虫'
        verbose_name_plural = '爬虫'


class DatabaseType(models.Model):
    DBname = models.CharField(max_length=50)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.DBname.encode('utf-8')

    class Meta:
        verbose_name = '数据库类型'
        verbose_name_plural = '数据库类型'





