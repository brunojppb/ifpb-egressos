from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from portal_do_egresso import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'portal_do_egresso.ifpb.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', 'portal_do_egresso.ifpb.views.register', name='register'),
    url(r'^login/$', 'portal_do_egresso.ifpb.views.home', name='home'),
    url(r'^logout/$', 'portal_do_egresso.ifpb.views.logout', name='logout'),
    url(r'^done/$', 'portal_do_egresso.ifpb.views.done', name='done'),
    url(r'^foto/$', 'portal_do_egresso.ifpb.views.foto', name='foto'),
    url(r'^complement/$', 'portal_do_egresso.ifpb.views.confirmar_dados', name='confirmar_dados'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'adm/', include('portal_do_egresso.administracao.urls'), name='adm'),
)

#habilita aexibicao das imagens salvas
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
