from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='pages_index'),
    url(r'^about/?$', views.about, name='pages_about'),
	url(r'^contact/?$', views.contact, name='pages_contact'),
	url(r'^info/?$', views.info, name='pages_info'),
	url(r'^downloads/?$', views.downloads, name='pages_downloads'),
	url(r'^theory/?$', views.theory, name='pages_theory'),
	url(r'^procedure/?$', views.procedure, name='pages_procedure'),
	url(r'^experiments/?$', views.experiments, name='pages_experiments'),
	url(r'^feedback/?$', views.feedback, name='pages_feedback'),
	url(r'^quiz/?$', views.quiz, name='pages_quiz'),
]