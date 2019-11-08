from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def signupPage(request):
    template = loader.get_template('signup/signup.html')
    return HttpResponse(template.render({}, request))