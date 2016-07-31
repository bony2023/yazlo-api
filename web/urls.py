from django.conf.urls import url, include
import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^verifycaptcha$', views.verifycaptcha),
	url(r'^verifyuser/(?P<token>\w{28})/$', views.verifyuser),
]
