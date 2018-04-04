from __future__ import unicode_literals
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from users.models import UserProfile
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django import forms
from .forms import UserProfileForm
import plaid
from plaid import Client
from plaid.errors import APIError, ItemError
import datetime


PLAID_CLIENT_ID = 'x'
PLAID_SECRET = 'x'
PLAID_PUBLIC_KEY = 'x'
PLAID_ENV = 'sandbox'



client = plaid.Client(client_id = PLAID_CLIENT_ID, secret=PLAID_SECRET,
                  public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)

@csrf_exempt
@login_required
def plaidstart(request):
    context = {'plaid_public_key': PLAID_PUBLIC_KEY, 'plaid_environment': PLAID_ENV}
    return render(request, 'dashboard/plaid/plaid.html', context)

access_token = None
public_token = None


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

start_date = "2017-05-05"
end_date = "2018-03-27"
@csrf_exempt
def transactions(request):
    if request.user.is_authenticated:
        
        global access_token
        print(access_token)
        # Pull transactions for the last 30 days
        start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
        end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())
        response = client.Transactions.get(access_token, start_date, end_date)
        print(response)
        return JsonResponse(response)
        #response = transactions.self
        transactions.save()
        print(response)
    
    
"""
@app.route("/create_public_token", methods=['GET'])
def create_public_token():
  global access_token
  # Create a one-time use public_token for the Item. This public_token can be used to
  # initialize Link in update mode for the user.
  response = client.Item.public_token.create(access_token)
  return jsonify(response)

"""