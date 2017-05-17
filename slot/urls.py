from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='slot_index'),
    url(r'^new/?$', views.new, name='slot_new'),
    url(r'^show/(.*)/?$', views.show, name='slot_show'),
    url(r'^create/?$', views.create, name='slot_create'),
    url(r'^delete/([0-9]+)/?$', views.delete, name='slot_delete'),
]