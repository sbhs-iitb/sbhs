from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.new, name='password_index'), 
    url(r'^link/?$', views.email, name='password_link'), 
    url(r'^edit/(.*)/?$', views.edit, name='password_edit'), 
    url(r'^update/(.*)/?$', views.update, name='password_update'), 
]