from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^admin/?$', views.index, name='admin_index'),
    url(r'^admin/bookings/?$', views.booking_index, name='admin_bookings'),
    url(r'^admin/webcam/?$', views.webcam_index, name='admin_webcam'),
    url(r'^admin/profile/([0-9]+)/?$', views.profile, name='admin_profile'),
    url(r'^admin/testing/?$', views.testing, name='admin_testing'),
    url(r'^admin/resetdevice/?$', views.reset_device, name='admin_reset_device'),
    url(r'^admin/setdevice/?$', views.set_device_params, name='admin_set_device'),
    url(r'^admin/gettemp/?$', views.get_device_temp, name='admin_get_temp'),
    url(r'^admin/monitor/?$', views.monitor_experiment, name='admin_monitor'),
    url(r'^admin/logs/([0-9]+)/?$', views.download_log, name='admin_logs'),
    url(r'^admin/updatemid/?$', views.update_allocated_mid, name='admin_updatemid'),
    url(r'^admin/changemid/?$', views.get_allocated_mids, name='admin_getmids'),
    url(r'^admin/getusers/?$', views.get_users, name='admin_users'),
    url(r'^admin/toggledevice', views.toggle_device_status, name='toggle_status'),
    url(r'^admin/viewlogs/?$', views.logs_index, name='admin_viewlogs'),
    url(r'^admin/rangelogs/?$', views.range_logs, name='admin_range_logs'),
    url(r'^admin/explogs/([0-9]+)/?$', views.download_experiment_log, name='admin_explogs'),
    
    url(r'^admin/toggle_allotment_mode/?$', views.toggle_allotment_mode, name='admin_toggle_allotment_mode'),
]
