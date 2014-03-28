from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'portal_do_egresso.administracao.views.convidar_cadastrados', name='convidar_cadastrados'),
)