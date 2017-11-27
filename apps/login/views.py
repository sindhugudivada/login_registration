from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'login/index.html')

def register(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user=User.objects.create(fname=fname,lname=lname,email=email,password=hash1)

    errors = User.objects.basic_validator_registration(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    request.session['user_id'] = user.id
    return redirect('/success')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    errors = User.objects.basic_validator_login(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        user=User.objects.get(email = request.POST['email'])
        request.session['user_id']=user.id
        return redirect('/success')

def success(request):
    try:
        request.session['user_id']
    except:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "login/success.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')   
