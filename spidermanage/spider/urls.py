#coding=utf-8

from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.spiderstatus, name='spiderstatus'),
    url(r'^spiderstatus$', views.spiderstatus, name='spiderstatus'),
    url(r'^checktask$', views.checktask, name='checktask'),

    url(r'^runtask$', views.runtask, name='runtask'),
    url(r'^runtask/startspider$', views.startspiderbyid, name='startspiderbyid'),
    url(r'^runtask/stopspider$', views.stopspiderbyid, name='stopspiderbyid'),

    url(r'^runtask/selectspider$', views.selectspiderbyid, name='selectspiderbyid'),
    url(r'^runtask/getspiderlog$', views.getspiderlogbyid, name='getspiderlogbyid'),

    # 根据爬虫id进入爬虫
    url(r'^s/(\d+)$', views.intospider, name='intospider'),
    url(r'^ss$', views.intospider_form, name='intospider_form'),

    url(r'^dataoprate$', views.dataoprate, name='dataoprate'),
    url(r'^data/(.*?)!(.*?)$', views.data_file_download, name='data_file_download'),
    url(r'^dataopinfo$', views.dataopinfo, name='dataopinfo'),

    url(r'^spidersetting$', views.spidersetting, name='spidersetting'),

    # url(r'^spiderhistoty$', views.spiderhistoty, name='spiderhistoty'),
    url(r'^spiderhistoty/(\d*)$', views.spiderhistoty, name='spiderhistoty'),

    url(r'^checkrunstatus$', views.checkrunstatus, name='checkrunstatus'),
]