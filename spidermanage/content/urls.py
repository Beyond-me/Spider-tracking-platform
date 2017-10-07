from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    # url(r'^articel$', views.articelpage, name='articelpage'),
    url(r'^articel/(\d*)$', views.articelpage, name='articelpage'),

    url(r'^articel/type/(.*?)$', views.choosetype, name='choosetype'),
    url(r'^a/(\d+)', views.articeldetail, name='articeldetail'),
]