from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^show_video/?$', views.show_video, name='webcam_show_video'),
	url(r'^reload_image/(.*)/?$', views.reload, name='webcam_reload_image'),
	url(r'^admin/webcam/([0-9]+)/?$', views.show_video_to_admin, name='webcam_show_video_to_admin'),
]