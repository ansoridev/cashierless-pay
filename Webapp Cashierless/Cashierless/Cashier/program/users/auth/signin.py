from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from .... import models as db
import json

def controller(request):
    return redirect('/home/') if request.session.get('email', '') else views(request) if request.method == 'GET' else ajax(request)

def views(request):
    return render(request, 'auth/signin.html')

def ajax(request):
    result = {
        "status": False
    }
    
    if request.is_ajax():
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        query = db.User.objects.filter(email=email)
        if query.exists():
            check = check_password(password, query[0].password)
            if check:
                result['status'] = check
                request.session['email'] = email
                
    return JsonResponse(result)