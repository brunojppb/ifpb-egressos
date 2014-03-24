from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'portal_do_egresso.ifpb.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup-email/', 'portal_do_egresso.ifpb.views.signup_email'),
    url(r'^email-sent/', 'portal_do_egresso.ifpb.views.validation_sent'),
    url(r'^login/$', 'portal_do_egresso.ifpb.views.home'),
    url(r'^logout/$', 'portal_do_egresso.ifpb.views.logout'),
    url(r'^done/$', 'portal_do_egresso.ifpb.views.done', name='done'),
    url(r'^email/$', 'portal_do_egresso.ifpb.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))

)
