from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'cc_mining.views.home', name='home'),
)
