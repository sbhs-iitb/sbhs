from django.conf.urls import url

from . import views

urlpatterns = [
	 # Following to are for backward incompatibility
    url(r'^hardware/checkconnection/?$', views.check_connection, name='hardware_checkconnection'),
    url(r'^hardware/clientversion/?$', views.client_version, name='hardware_clientversion'),

    url(r'^experiment/check_connection/?$', views.check_connection, name='experiment_check_connection'),
    url(r'^experiment/client_version/?$', views.client_version, name='experiment_client_version'),
    url(r'^experiment/initiate/?$', views.initiation, name='experiment_initiate'),
    url(r'^experiment/experiment/?$', views.experiment, name='experiment_experiment'),
    url(r'^experiment/reset/?$', views.reset, name='experiment_reset'),
    url(r'^experiment/logs/?$', views.logs, name='experiment_logs'),
    url(r'^experiment/logs/([0-9]+)/(.+)?$', views.download_log, name='experiment_logs'),

    url(r'^admin/validate_log_file/?$', views.validate_log_file, name='experiment_validate_log'),
]