from django.urls import path
from .views import plaidstart, get_access_token, accounts, transactions, daily_transactions

urlpatterns = [
    path('dashboard/plaid/', plaidstart, name='plaidstart'),
    path('get_access_token', get_access_token, name='get_access_token'),
    path('accounts', accounts, name='accounts'),
    path('transactions', transactions, name='transactions'),
    path('daily_transactions', daily_transactions, name='daily_transactions'),
]

