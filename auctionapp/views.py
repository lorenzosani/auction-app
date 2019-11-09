from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.db import IntegrityError
import datetime as D

from auctionapp.models import Member


# --- Pages ----
def signupPage(request):
    template = loader.get_template('signup/index.html')
    return HttpResponse(template.render({}, request))

def loginPage(request):
    template = loader.get_template('login/index.html')
    return HttpResponse(template.render({}, request))

# ---- Requests ---- 
def signupRequest(request):
    if 'email' in request.POST:
        email = request.POST['email']

    if 'dateOfBirth' in request.POST:
        date_of_birth = request.POST['dateOfBirth']

    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        pw = request.POST['password']

        user = Member(username=username, email=email, date_of_birth=date_of_birth)
        user.set_password(pw)
        
        try: user.save()
        except IntegrityError: raise Http404('Username {} already taken: Usernames must be unique'.format(username))
        return JsonResponse({'username': username})

    else:
        raise Http404('Missing required POST data.')

def loginRequest(request):
    username = request.POST['loginId']
    password = request.POST['loginPw']
    
    try: member = Member.objects.get(username=username)
    except Member.DoesNotExist: raise Http404('User not found')
    
    if member.check_password(password):
        # remember user in session variable
        request.session['username'] = username
        request.session['password'] = password
        context = {
            'username': username,
            'loggedin': True
        }
        response = render(request, 'login/index.html', context)

        now = D.datetime.utcnow()
        # 1 week. d * h  * m  * s
        max_age = 7 * 24 * 60 * 60
        delta = now + D.timedelta(seconds=max_age)
        format = "%a, %d-%b-%Y %H:%M:%S GMT"
        expires = D.datetime.strftime(delta, format)
        # Set a "last_login" cookie that expires in max_age
        response.set_cookie('last_login', now, expires=expires)
        return response

    else:
        # Vague error message to avoid giving away too much info
        raise Http404('Wrong username or password.')

# TODO Add isLoggedIn decorator to check if a user is logged in.