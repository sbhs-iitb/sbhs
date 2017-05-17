from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^admin/?$', views.index, name='admin_index'),
    url(r'^admin/bookings/?$', views.booking_index, name='admin_bookings'),
    url(r'^admin/webcam/?$', views.webcam_index, name='admin_webcam'),
    url(r'^admin/profile/([0-9]+)/?$', views.profile, name='admin_profile'),
    
    url(r'^admin/toggle_allotment_mode/?$', views.toggle_allotment_mode, name='admin_toggle_allotment_mode'),
]