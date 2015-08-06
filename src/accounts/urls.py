from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^signup$', 'accounts.views.signup', name='signup'),
    url(r'^login$', 'accounts.views.userLogin', name='login'),
    url(r'^logout$', 'accounts.views.userLogout', name='logout'),
    url(r'^changePassword$', 'accounts.views.changePassword', name='changepassword'),
    url(r'^forgotPassword$', 'accounts.views.forgotPassword', name='forgotpassword'),
    url(r'^uploadprofilepicture', 'accounts.views.ProfilePictureUpload', name='uploadprofilepicture'),

)