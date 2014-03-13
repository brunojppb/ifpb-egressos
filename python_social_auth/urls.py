from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'python_social_auth.ifpb.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup-email/', 'python_social_auth.ifpb.views.signup_email'),
    url(r'^email-sent/', 'python_social_auth.ifpb.views.validation_sent'),
    url(r'^login/$', 'python_social_auth.ifpb.views.home'),
    url(r'^logout/$', 'python_social_auth.ifpb.views.logout'),
    url(r'^done/$', 'python_social_auth.ifpb.views.done', name='done'),
    url(r'^email/$', 'python_social_auth.ifpb.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))

)
