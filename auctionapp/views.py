from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.db import IntegrityError

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