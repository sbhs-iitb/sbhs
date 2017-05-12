from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sbhs_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', 'sbhs_server.pages.views.index'),
    url(r'^exam/', include('yaksh.urls')),
    url(r'^about/?$', 'sbhs_server.pages.views.about'),
    url(r'^contact/?$', 'sbhs_server.pages.views.contact'),
    url(r'^info/?$', 'sbhs_server.pages.views.info'),
    url(r'^downloads/?$', 'sbhs_server.pages.views.downloads'),
    url(r'^theory/?$', 'sbhs_server.pages.views.theory'),
    url(r'^procedure/?$', 'sbhs_server.pages.views.procedure'),
    url(r'^experiments/?$', 'sbhs_server.pages.views.experiments'),
    url(r'^feedback/?$', 'sbhs_server.pages.views.feedback'),
    url(r'^quiz/?$', 'sbhs_server.pages.views.quiz'),
    
    url(r'^enter/?$', 'sbhs_server.account.views.index'),
    url(r'^account/create/?$', 'sbhs_server.account.views.create'),
    url(r'^account/confirm/(.*)/?$', 'sbhs_server.account.views.confirm'),
    url(r'^login/?$', 'sbhs_server.account.views.login'),
    url(r'^logout/?$', 'sbhs_server.account.views.logout'),
    url(r'^home/?$', 'sbhs_server.account.views.home'),

    url(r'^password/?$', 'sbhs_server.password.views.new'),
    url(r'^password/link/?$', 'sbhs_server.password.views.email'),
    url(r'^password/edit/(.*)/?$', 'sbhs_server.password.views.edit'),
    url(r'^password/update/(.*)/?$', 'sbhs_server.password.views.update'),

    url(r'^slot/?$', 'sbhs_server.slot.views.index'),
    url(r'^slot/new/?$', 'sbhs_server.slot.views.new'),
    url(r'^slot/show/(.*)/?$', 'sbhs_server.slot.views.show'),
    url(r'^slot/create/?$', 'sbhs_server.slot.views.create'),
    url(r'^slot/delete/([0-9]+)/?$', 'sbhs_server.slot.views.delete'),

    # Following to are for backward incompatibility
    url(r'^hardware/checkconnection/?$', 'sbhs_server.experiment.views.check_connection'),
    url(r'^hardware/clientversion/?$', 'sbhs_server.experiment.views.client_version'),

    url(r'^experiment/check_connection/?$', 'sbhs_server.experiment.views.check_connection'),
    url(r'^experiment/client_version/?$', 'sbhs_server.experiment.views.client_version'),
    url(r'^experiment/initiate/?$', 'sbhs_server.experiment.views.initiation'),
    url(r'^experiment/experiment/?$', 'sbhs_server.experiment.views.experiment'),
    url(r'^experiment/reset/?$', 'sbhs_server.experiment.views.reset'),
    url(r'^experiment/logs/?$', 'sbhs_server.experiment.views.logs'),
    url(r'^experiment/logs/([0-9]+)/(.+)?$', 'sbhs_server.experiment.views.download_log'),

    url(r'^show_video/?$', 'sbhs_server.webcam.views.show_video'),
    url(r'^reload_image/(.*)/?$', 'sbhs_server.webcam.views.reload'),

    url(r'^admin/?$', 'sbhs_server.admin.views.index'),
    url(r'^admin/bookings/?$', 'sbhs_server.admin.views.booking_index'),
    url(r'^admin/webcam/?$', 'sbhs_server.admin.views.webcam_index'),
    url(r'^admin/profile/([0-9]+)/?$', 'sbhs_server.admin.views.profile'),
    url(r'^admin/webcam/([0-9]+)/?$', 'sbhs_server.webcam.views.show_video_to_admin'),
    url(r'^admin/toggle_allotment_mode/?$', 'sbhs_server.admin.views.toggle_allotment_mode'),
    url(r'^admin/validate_log_file/?$', 'sbhs_server.experiment.views.validate_log_file'),
)

handler404 = 'sbhs_server.pages.views.e404'
handler500 = 'sbhs_server.pages.views.e500'
