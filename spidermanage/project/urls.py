from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.project, name='project'),
    url(r'^p/(.*?)$', views.projectdetail, name='projectdetail'),
    url(r'^ptype/(.*?)$', views.ptype, name='ptype'),
]