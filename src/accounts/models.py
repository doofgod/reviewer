
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#class User(models.Model):
#    email = models.EmailField(primary_key=True)
#    last_login = models.DateTimeField(default=timezone.now)
#    REQUIRED_FIELDS = ()
#    USERNAME_FIELD = 'email'
    
#    def is_authenticated(self):
#        return True
    
    
class UserProfilePicture(models.Model):
    userFK = models.ForeignKey(User, default ="1")
    image = models.ImageField(upload_to='profiles')
    