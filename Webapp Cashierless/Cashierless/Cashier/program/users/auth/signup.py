from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .... import models as db
import json

def controller(request):
    return redirect('/home/') if request.session.get('email', '') else views(request) if request.method == 'GET' else ajax(request)

def views(request):
    return render(request, 'auth/signup.html')

def ajax(request):
    result = {
        "status": False
    }
    
    if request.is_ajax():
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password = make_password(request.POST.get('password', ''), hasher="pbkdf2_sha256")
        query = db.User.objects.filter(email=email)
        if not query.exists():
            db.User(
                name = name,
                email = email,
                password = password,
                balance = 0
            ).save()
            request.session['email'] = email
            result['status'] = True
                
    return JsonResponse(result)