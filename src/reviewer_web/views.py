from django.shortcuts import render
from django.core.files import File
#from django.core.files.storage import FileSystemStorage
from django.core.files.images import get_image_dimensions
#from models import UserProfilePicture
from accounts.models import UserProfilePicture
from accounts.views import getProfilePicture
from django.contrib.auth.models import User
#from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
import urllib2

import os
import json
from reviewer.settings import MEDIA_ROOT, MEDIA_URL


def home_page(request):
    if request.user.is_authenticated():
#        print request.user.id
#        print os.path.dirname(os.path.abspath(__file__))
#        print __file__
        print 'user is authenticated in the home page'

        userImageName = getProfilePicture(request.user.id)

        print MEDIA_URL
        print str(userImageName)
        home_url = "http://127.0.0.1:8000"
        return render(request, 'home.html', {'picture':userImageName, 'home_url': home_url,\
                                                     'MEDIA_URL': MEDIA_URL})
         
    else:
        return render(request, 'signup.html')
