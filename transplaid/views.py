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


@csrf_exempt
@login_required
def daily_transactions(request, *args, **kwargs):
    all_transactions = {}
    users_without_valid_access_tokens = []
    if request.user.is_authenticated:
        users = UserProfile.objects.exclude(access_token__isnull=True).exclude(access_token__exact='')
        for u in users:
            # Pull transactions for the last 30 days
            start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-1))
            end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())            
            try:
                response = client.Transactions.get(u.access_token, start_date, end_date)
            except plaid.errors.InvalidInputError: 
                users_without_valid_access_tokens.append(u.user.username)
                continue
            # gettings transactions from the response
            serialized = [TransactionSerializer(data=t) for t in response.get("transactions", [])]
            for transaction in serialized:
                if transaction.is_valid():
                    transaction.save(owner=request.user, created=timezone.now())
            all_transactions[u.access_token] = response.get("transactions")
        return JsonResponse({
            "users_without_valid_access_tokens": users_without_valid_access_tokens,
            "transactions": all_transactions
        })


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
            print(request.user.id)
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.access_token = access_token
            profile.item_id = item_id
            profile.save()

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
