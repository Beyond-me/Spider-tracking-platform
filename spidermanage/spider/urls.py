from django.conf.urls import url
import views


urlpatterns = [
    url(r'^spiderstatus$', views.spiderstatus, name='spiderstatus'),
    url(r'^checktask$', views.checktask, name='checktask'),

    url(r'^runtask$', views.runtask, name='runtask'),
    url(r'^runtask/startspider$', views.startspiderbyid, name='startspiderbyid'),
    url(r'^runtask/selectspider$', views.selectspiderbyid, name='selectspiderbyid'),
    url(r'^runtask/getspiderlog$', views.getspiderlogbyid, name='getspiderlogbyid'),

    url(r'^dataoprate$', views.dataoprate, name='dataoprate'),
    url(r'^spidersetting$', views.spidersetting, name='spidersetting'),
    url(r'^spiderhistoty$', views.spiderhistoty, name='spiderhistoty'),
]