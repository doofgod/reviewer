from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'reviewer_web.views.home_page', name='home'),
    url(r'^accounts/', include('accounts.urls')),
)
