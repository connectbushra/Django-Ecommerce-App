from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .helpers import forget_password_mail
from django.conf import settings
from .models import Profile
import uuid


def login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password1']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'invalid username/password...')
                return render(request, "login.html")
        else:
            messages.warning(request,"To continue , you must login first ")
            return render(request, "login.html")
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email =request.POST['email']
        password =request.POST['password1']
        re_password =request.POST['password2']
        if password == re_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'username alreday exist')
                return redirect('account:register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email alreday exist')
                return redirect('account:register')
            else:
                user =User.objects.create_user(username=username,email=email,password=password)
                user.save();
                return redirect('/')
        else:
            messages.warning(request,'Password not Matching......')
            return redirect('account:register')
    else:
     return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def Reset_password(request,token):
    context={}
    profile_obj= Profile.objects.filter(forget_password_token=token)
    print(profile_obj)
    context = {'user_id': profile_obj}
    if request.method == 'POST':
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')
        user_id=request.POST.get('user_id')
        print('.............')
        if user_id is None:
            messages.success(request,"No user id found")
            return redirect(f'/change_password/{token}/')
        if new_password != confirm_password:
            messages.warning(request,"Password not matching....")
            return redirect(f'/change_password/{token}/')
        user_obj=User.objects.get(id=user_id)
        user_obj.set_password (new_password)
        user_obj.save()
        return redirect('account:login')
    context = {'user_id' :profile_obj}
    return render(request, "change_password.html",context)

def forget_password(request):
    if request.method=='POST':
        email = request.POST.get('email')
        if not User.objects.filter(email=email).first() :
            print("fail...........")
            messages.warning(request,"This email is not registered")
            return redirect('account:forget_password')

        user_obj=User.objects.get(email=email)
        token=str(uuid.uuid4())
        forget_password_mail(user_obj,token)
        print(forget_password_mail)
        messages.success(request,"Email has been sent...")
        return redirect('account:forget_password')
    return render(request,"forget_password.html")




