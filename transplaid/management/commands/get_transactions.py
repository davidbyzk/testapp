from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import plaid

from transplaid import views

class Command(BaseCommand):
    help = 'Retrieves transactions for users with active access tokens'

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super().__init__(stdout, stderr, no_color)
        self.client = plaid.Client(client_id = settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET, 
        public_key=settings.PLAID_PUBLIC_KEY, environment=settings.PLAID_ENV)

    def handle(self, *args, **options):
        users_without_access_token, all_transactions = views.get_users_transactions(self.client)
        if users_without_access_token:
            self.stdout.write(self.style.ERROR("Users with not valid access tokens found:"))
            for u in users_without_access_token:
                self.stdout.write(self.style.ERROR(u))
        self.stdout.write(self.style.SUCCESS("Fetched: %s transactions" % len(all_transactions)))