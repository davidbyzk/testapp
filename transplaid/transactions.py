import datetime
from dateutil import relativedelta
from django.db.utils import IntegrityError
from django.utils import timezone
from users.models import UserProfile
from transplaid.serializers import TransactionSerializer, InitialPullTransactionSerializer
import plaid

TRANSACTIONS_TO_FETCH = 500

def get_users_transactions(client):
    users = UserProfile.objects.exclude(
        access_token__isnull=True).exclude(access_token__exact='')
    users_without_valid_access_tokens = []
    all_transactions = {}
    for u in users:
        start_date = "{:%Y-%m-%d}".format(
            datetime.datetime.now() + datetime.timedelta(-1))
        end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())
        try:
            response = client.Transactions.get(
                u.access_token, start_date, end_date)
        except plaid.errors.InvalidInputError:
            users_without_valid_access_tokens.append(u.user.username)
            continue
        # gettings transactions from the response
        serialized = [TransactionSerializer(data=t)
                      for t in response.get("transactions", [])]
        for transaction in serialized:
            if transaction.is_valid():
                transaction.save(owner=u.user, created=timezone.now())
        all_transactions[u.access_token] = response.get("transactions")
    return users_without_valid_access_tokens, all_transactions


def get_initial_pull_transactions(client):
    users = UserProfile.objects.filter(just_signed_up=True).exclude(
        access_token__isnull=True).exclude(access_token__exact='')
    users_without_valid_access_tokens = []
    all_transactions = {}
    count = TRANSACTIONS_TO_FETCH    
    for u in users:
        offset = 0
        start_date = "{:%Y-%m-%d}".format(
            datetime.date.today() + relativedelta.relativedelta(years=-2))
        end_date = "{:%Y-%m-%d}".format(datetime.date.today())
        try:
            response = client.Transactions.get(
                u.access_token, start_date, end_date,
                count=count, offset=offset)
        except plaid.errors.InvalidInputError:
            users_without_valid_access_tokens.append(u.user.username)
            continue
        total_transactions = response.get("total_transactions")
        all_transactions[u] = response.get("transactions", [])
        offset += count
        while offset < total_transactions:
            response = client.Transactions.get(
                u.access_token, start_date, end_date,
                count=TRANSACTIONS_TO_FETCH, offset=offset)
            all_transactions[u].append(response.get("transactions", []))
            offset += count
    for u, transactions in all_transactions.items():
        for user_transaction in transactions:
            deserialized = InitialPullTransactionSerializer(data=user_transaction)
            if deserialized.is_valid():
                deserialized.save(owner=u.user, created=timezone.now())
        u.just_signed_up = False
        u.save()

    return users_without_valid_access_tokens
