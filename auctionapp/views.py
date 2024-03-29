from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.db import IntegrityError
from django.conf import settings
from PIL import Image
from decimal import Decimal
import datetime as D
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.template.defaulttags import register

from auctionapp.models import Member, Item, Bid
from auctionapp.forms import NewItemForm
from auctionapp.serializers import ActiveAuctionsSerializer

# --- Pages ----
def signupPage(request):
    template = loader.get_template('signup/index.html')
    return HttpResponse(template.render({}, request))

def loginPage(request):
    template = loader.get_template('login/index.html')
    return HttpResponse(template.render({}, request))

@login_required
def profilePage(request, username):
    logged_user = request.user.username
    if logged_user != username:
        raise Http404('Not your profile, sorry.')
    template = loader.get_template('user_profile/index.html')
    user_info = Member.objects.get(username=username)
    user_bids = Bid.objects.filter(bidder=user_info)
    # Get auctions won in the past 24 hours
    items_ended_today = Item.objects.filter(end_time__lt=timezone.now(), end_time__gt=timezone.now() - D.timedelta(1))
    bids_won_today = []
    for item in items_ended_today:
      winning_bid = item.bid_set.first()
      if winning_bid:
        winner = winning_bid.bidder
        if username == winner.username:
            bids_won_today.append(winning_bid)
    return HttpResponse(template.render({"userInfo": user_info, "bids": user_bids, "bidsWon": bids_won_today}, request))

def pwResetSentPage(request):
    template = loader.get_template('reset_pw/done.html')
    return HttpResponse(template.render({}, request))

def pwResetCompletedPage(request):
    template = loader.get_template('reset_pw/complete.html')
    return HttpResponse(template.render({}, request))

def itemDetail(request, item_id):
    item = Item.objects.get(id=item_id)
    # Get buyer
    try:
        bidsList = list(item.bid_set.all())
        buyer = str(bidsList[0].bidder).split(' ')[1]
    except:
        buyer = None
    data = { 
        "item": item,
        "image": item.image,
        "closed": item.end_time < timezone.now(),
        "price": _get_current_price(item),
        "buyer": buyer,
    }
    template = loader.get_template('item_page/index.html')
    return HttpResponse(template.render(data, request))

def itemsList(request):
    items = Item.objects.filter(end_time__gt=timezone.now())
    template = loader.get_template('items_list/index.html')
    context = { "items": items }
    return HttpResponse(template.render(context, request))

@login_required
def closedItems(request):
    closed_items = Item.objects.filter(end_time__lt=timezone.now())
    bidsByItem = {}
    for item in closed_items:
        # Build the dictionary
        if str(item.id) not in bidsByItem:
            bidsByItem[str(item.id)] = {}
        bidsByItem[str(item.id)] = list(item.bid_set.all())
    template = loader.get_template('closed_items/index.html')
    context = { "items": closed_items, "bidsByItem": bidsByItem }
    return HttpResponse(template.render(context, request))

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
    user = authenticate(username=username, password=password)    
    if user is not None:
        # Login user
        login(request, user)
        context = {
            'username': username,
            'loggedin': True
        }
        response = JsonResponse(context)
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

def logoutRequest(request):
    logout(request)
    return redirect(itemsList)

@login_required
def addNewItem(request):
    if request.method == 'POST':
        # Get form data and item image
        f = NewItemForm(request.POST, request.FILES)
        # Validate and format input
        if f.is_valid():
            form = f.cleaned_data
            # Create new item and save in db
            item = Item(title=form['title'], description=form['description'], image=form['image'], start_price=form['start_price'], end_time=form['end_time'])
            item.save()
            return HttpResponseRedirect('/item/{}'.format(item.id))
        else:
            return HttpResponse('The form is not valid')
    else:
        form = NewItemForm()
        template = loader.get_template('new_item/index.html')
        return HttpResponse(template.render({'form': form}, request))

def makeBid(request, item_id):
    # Check if user is logged in
    if not request.user.is_authenticated:
        response = JsonResponse({"error": "You must log in to place a bid"})
        response.status_code = 403
        return response  
    user = Member.objects.get(username=request.user.username)
    item = Item.objects.get(id=item_id)
    price = Decimal(request.POST['price'])
    # Check if price of bid is valid
    if price <= item.start_price or price<=_get_current_price(item):
        response = JsonResponse({"error": "The bid must be higher than the current price"})
        response.status_code = 403
        return response
    bid = Bid(bidder=user, item=item, amount=price)
    bid.save()
    data = { "new_price": bid.amount, "buyer": str(bid.bidder).split(" ")[1] }
    return JsonResponse(data)

# ---- Helper methods ---- 
def _get_current_price(item):
    bids = Bid.objects.filter(item=item)
    if bids.count() == 0:
        return item.start_price
    highest = None
    for bid in bids:
        if highest:
            if bid.amount>highest.amount:
                highest = bid
        else:
            highest = bid
    return highest.amount
        
# ---- API ----
class ActiveAuctionsViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(end_time__gt=timezone.now())
    serializer_class = ActiveAuctionsSerializer
 
    @action(detail=False)
    def search(self, request):
        _query = request.GET.get("q")
        # If we defined a query, filter items
        if _query is not None:
            filtered_items = Item.objects.all().filter(title__icontains=_query)
            filtered_desc = Item.objects.all().filter(description__icontains=_query)
            # Concatenate both results.
            filtered_items = list(filtered_items) + list(filtered_desc)
        # Otherwise return all items
        else:
            filtered_items = Item.objects.all()
        page = self.paginate_queryset(filtered_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(filtered_items, many=True)
        return Response(serializer.data)

# ---- Template filters ----
@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))