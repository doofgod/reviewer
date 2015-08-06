from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, hashers
from forms import UserForm, LoginForm, PasswordChangeForm, ForgotPasswordForm, UploadProfilePictureForm
from django.core.files.images import get_image_dimensions
from phagebook.settings import MEDIA_ROOT, MEDIA_URL
from models import UserProfilePicture
import os 
from django.conf import settings
from django.core.mail import send_mail



def signup(request):

    if request.method == 'POST':
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            username = userForm.cleaned_data['username']
            password = userForm.cleaned_data['password']
            email = userForm.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            messages =[]
            messages.append('User added')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            #need to add something here to return the image
            return render(request, 'homeLoggedIn.html',{'messages': messages})
            
    else:
        userForm = UserForm()
        return render(request, 'signup.html',{'userForm': userForm})


def changePassword(request):
    # This needs work
    messages = [] 
    if request.method == 'POST':
        print request.POST
        passwordChangeForm = PasswordChangeForm(request.POST)
        if passwordChangeForm.is_valid():
            if hashers.check_password(passwordChangeForm.cleaned_data['oldpassword'], request.user.password):

                if passwordChangeForm.cleaned_data['newpassword1'] == passwordChangeForm.cleaned_data['newpassword2']:
                    request.user.set_password(passwordChangeForm.cleaned_data['newpassword1'])
                    request.user.save()
                    print 'password change request successful'
                    return render(request, 'changePassword.html', {'passwordChangeForm':passwordChangeForm,\
                                                               'messages':messages})
                else: 
                    messages.append('passwords do not match')  
                    passwordChangeForm = PasswordChangeForm()
                    return render(request, 'changePassword.html', {'passwordChangeForm':passwordChangeForm,\
                                                   'messages':messages})
            else:
                messages.append('Bad password supplied')
                passwordChangeForm = PasswordChangeForm()
                return render(request, 'changePassword.html', {'passwordChangeForm':passwordChangeForm,\
                                                               'messages':messages}) 
        
        else:
            messages.append('form is not valid')
            passwordChangeForm = PasswordChangeForm()
            return render(request, 'changePassword.html', {'passwordChangeForm':passwordChangeForm,\
                                                               'messages':messages})

    else:
        passwordChangeForm = PasswordChangeForm()   
        return render(request, 'changePassword.html', {'passwordChangeForm':passwordChangeForm,\
                                                       'messages':messages})
    



def userLogin(request):
    messages =[]
    if request.method == 'POST':
            loginForm = LoginForm(request.POST)
            if loginForm.is_valid():
                user = authenticate(username = loginForm.cleaned_data['username'],\
                                    password = loginForm.cleaned_data['password'])
                
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.append('login successful')
                        return render(request, 'homeLoggedIn.html', {'messages':messages})
                    else:
                        messages.append('login failed: user is not active')
                        loginForm = LoginForm()
                        return render(request, 'signup.html', {'loginForm':loginForm,'messages':messages})
                        # Return a 'disabled account' error message
                        
                else:
                    messages.append("Bad user name and password combination")
                    loginForm = LoginForm()
                    return render(request, 'login.html', {'loginForm':loginForm,'messages':messages})
            else:
                messages.append('Invalid form')
                loginForm = LoginForm()
                return render(request, 'login.html',{'loginForm': loginForm,'messages':messages})
    else:
        loginForm = LoginForm()
        return render(request, 'login.html',{'loginForm': loginForm})
        
        
def userLogout(request):
    logout(request)

    print 'logout successful'
    return render(request, 'homeNotLoggedIn.html')
    
def forgotPassword(request):
    messages = []
    if request.method == 'POST':
        
        forgotPasswordForm = ForgotPasswordForm(request.POST)
        if forgotPasswordForm.is_valid():
            try:
                user= User.objects.get(username= forgotPasswordForm.cleaned_data['username'])
                print user 
                print user.email
                messages.append('user found, forgot password email to be sent')
#                send_mail('Subject here', 'Here is the message.', 'from@example.com',
#                          ['alexlee0227@gmail.com'], fail_silently=False)
                forgotPasswordForm = ForgotPasswordForm()
                return render(request,'ForgotPassword.html',{'forgotPasswordForm':forgotPasswordForm,'messages':messages})
            except User.DoesNotExist:
                messages.append('user not found')
                forgotPasswordForm = ForgotPasswordForm()
                return render(request,'ForgotPassword.html',{'forgotPasswordForm':forgotPasswordForm,'messages':messages})

        else:
            messages.append('invalid form')
            forgotPasswordForm = ForgotPasswordForm()
            return render(request,'ForgotPassword.html',{'forgotPasswordForm':forgotPasswordForm,'messages':messages})
            
    else: 
        forgotPasswordForm = ForgotPasswordForm()
        return render(request, 'ForgotPassword.html', {'forgotPasswordForm':forgotPasswordForm,'messages':messages})



def ProfilePictureUpload(request):
#    print request.user

# What if someone wants to update over an image that is already there? 
# What if someone tries to do the same file name?
# Restrictions on image size
    loggedUser = User.objects.get(pk = request.user.id)
    messages = []
#    print "logged user: " + str(loggedUser)
#    print "Is user authenticated: " +  str(request.user.is_authenticated())
    if request.user.is_authenticated():

#        try:
#            x3 = UserProfilePicture.objects.get(userFK = loggedUser)
#            print "Image file path: " + os.path.join(settings.MEDIA_ROOT,str(x3.image) )
#        except:
#            print None
        #os.remove(os.path.join(settings.MEDIA_ROOT,str(picture.image.name) ))
        if request.method == "POST":
            uploadProfilePictureForm = UploadProfilePictureForm(request.POST, request.FILES)
            filename = request.FILES['file']
            w, h = get_image_dimensions(filename)
            #print  "Filename: " + str(filename)
            print "width: " + str(w)
            print "height: " + str(w)
            try:
                x3 = UserProfilePicture.objects.get(userFK = loggedUser)
                os.remove(os.path.join(settings.MEDIA_ROOT,str(x3.image.name) ))
                x3.image = request.FILES['file']
            except UserProfilePicture.DoesNotExist:  
                x3 = UserProfilePicture.objects.create(userFK = loggedUser, image = request.FILES['file'])
     #       x3 = UserProfilePicture(userFK = loggedUser, image = request.FILES['file'])
            print "x3 image : " + str(x3.image)
            x3.save()
            messages.append('profile image saved')
            
            home_url = "http://127.0.0.1:8000"
            
            return render(request, 'homeLoggedIn.html', {'messages':messages})
        else:
            print request.user.id
            uploadProfilePictureForm=UploadProfilePictureForm()
            return render(request, 'MyProfile.html',{'uploadProfilePictureForm':uploadProfilePictureForm})

def getProfilePicture(requestUserID):
    
#    defaultImageFolder = MEDIA_ROOT + "\\" + str(userID) + "\\" + "profile"
    try:
        #userImageName = UserProfilePicture.objects.get(userID).image
        userImageName = UserProfilePicture.objects.get(userFK_id = requestUserID).image
        #print userImageName
    except UserProfilePicture.DoesNotExist:
        userImageName= "default.jpg"
        #print'cat'
    return userImageName