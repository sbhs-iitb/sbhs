from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^enter/?$', views.index, name='account_enter'),
    url(r'^account/create/?$', views.create, name='account_create'),
    url(r'^account/confirm/(.*)/?$', views.confirm, name='account_confirm'),
    url(r'^login/?$', views.login, name='account_login'),
    url(r'^logout/?$', views.logout, name='account_logout'),
    url(r'^home/?$', views.home, name='account_home'),
]