from __future__ import unicode_literals
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.utils import timezone
from django.conf import settings
from .forms import UserProfileForm
import plaid
from plaid import Client
from plaid.errors import APIError, ItemError
from .serializers import TransactionSerializer
from users.models import UserProfile
import datetime
import time

PLAID_CLIENT_ID = settings.PLAID_CLIENT_ID
PLAID_SECRET = settings.PLAID_SECRET
PLAID_PUBLIC_KEY = settings.PLAID_PUBLIC_KEY
PLAID_ENV = settings.PLAID_ENV

client = plaid.Client(client_id = PLAID_CLIENT_ID, secret=PLAID_SECRET,
                  public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)

@csrf_exempt
@login_required
def plaidstart(request):
    print(settings)
    context = {'plaid_public_key': PLAID_PUBLIC_KEY, 'plaid_environment': PLAID_ENV}
    return render(request, 'dashboard/plaid/plaid.html', context)

access_token = None
public_token = None


def get_intervals(day):
    
    time.mktime()

@csrf_exempt
@login_required
def get_transactions(request, *args, **kwargs):
    FRIDAY = 4
    friday_time = (16, 00)
    usual_time = (18, 00)
    launch_time = datetime.datetime.now()
    if datetime.weekday() == FRIDAY:
        start_date = .mk    
    if request.user.is_authenticated:
        users = UserProfile.objects.get()
        for u in users:
            response = client.Transactions.get(u.access_token, start_date, end_date)
            # Pull transactions for the last 30 days
            start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-1))
            end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())
            response = client.Transactions.get(access_token, start_date, end_date)
            # gettings transactions from the response
            serialized = [TransactionSerializer(data=t) for t in response.get("transactions", [])]
            for transaction in serialized:
                if transaction.is_valid():
                    transaction.save(owner=request.user, created=timezone.now())            


@csrf_exempt
@login_required
def get_access_token(request, *args, **kwargs):
    if request.method == 'POST':
        if request.user.is_authenticated:                 
            global access_token
            public_token = request.POST.get('public_token')
            exchange_response = client.Item.public_token.exchange(public_token)
            print('public token: ' + public_token)
            print('access token: ' + exchange_response['access_token'])
            print('item ID: ' + exchange_response['item_id'])

            access_token = exchange_response['access_token']
            item_id = exchange_response['item_id']
            print(item_id)
            print(exchange_response)  
           

            return JsonResponse(exchange_response)


@csrf_exempt
def accounts(request):
    if request.user.is_authenticated:
        obj = UserProfile()
        obj.access_token = access_token
        print(access_token)  
        
        accounts = client.Auth.get(access_token)
        print(accounts)
        return JsonResponse(accounts)

def item(request):
    global access_token
    item_response = client.Item.get(access_token)
    institution_response = client.Institutions.get_by_id(item_response['item']['institution_id'])
    return JsonResponse({'item': item_response['item'], 'institution': institution_response['institution']})

@csrf_exempt
def transactions(request):
    FRIDAY = 4
    friday_time = (16, 00)
    usual_time = (18, 00)    
    launch_time = datetime.datetime.now()
    if datetime.weekday() == FRIDAY:
        start_date = datetime.datetime.
    if request.user.is_authenticated:
        global access_token
        print(access_token)
        # Pull transactions for the last 30 days
        start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
        end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())
        response = client.Transactions.get(access_token, start_date, end_date)
        # gettings transactions from the response
        serialized = [TransactionSerializer(data=t) for t in response.get("transactions", [])]
        for transaction in serialized:
            if transaction.is_valid():
                transaction.save(owner=request.user, created=timezone.now())

        return JsonResponse(response)

"""
@app.route("/create_public_token", methods=['GET'])
def create_public_token():
  global access_token
  # Create a one-time use public_token for the Item. This public_token can be used to
  # initialize Link in update mode for the user.
  response = client.Item.public_token.create(access_token)
  return jsonify(response)

"""
