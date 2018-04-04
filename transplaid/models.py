from __future__ import unicode_literals
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from Lib.unittest.util import _MAX_LENGTH
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.conf import settings
       

   

class Public(models.Model):
    created = models.DateTimeField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='public_token', on_delete=models.CASCADE)
    public_token = models.CharField(max_length=100, blank=True, default='')
    request_id = models.CharField(max_length=25, blank=True, default='')
    
    class Meta:
        ordering = ('public_token',)
    

class Exchange(models.Model):
    created = models.DateTimeField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='token', on_delete=models.CASCADE)
    access_token = models.CharField(max_length=100, blank=True, default='')
    item_id = models.CharField(max_length=100, blank=True, default='')
    request_id = models.CharField(max_length=100, blank=True, default='')
    
    class Meta:
        ordering = ('item_id',)

class Transaction(models.Model):
    created = models.DateTimeField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transaction', on_delete=models.CASCADE)
    accounts = models.CharField(max_length=100, blank=True, default='')
    transactions = models.CharField(max_length=100, blank=True, default='')
    account_id = models.CharField(max_length=100, blank=True, default='')
    amount = models.CharField(max_length=100, blank=True, default='')
    category = models.CharField(max_length=100, blank=True, default='')
    category_id = models.CharField(max_length=100, blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    address =  models.CharField(max_length=100, blank=True, default='')
    city =  models.CharField(max_length=100, blank=True, default='')
    state =  models.CharField(max_length=100, blank=True, default='')
    lat =  models.CharField(max_length=100, blank=True, default='')
    lon =  models.CharField(max_length=100, blank=True, default='')
    name =  models.CharField(max_length=100, blank=True, default='')
    payment_meta = models.CharField(max_length=100, blank=True, default='')
    pending = models.CharField(max_length=100, blank=True, default='')
    pending_transaction_id = models.CharField(max_length=100, blank=True, default='')
    account_owner = models.CharField(max_length=100, blank=True, default='')
    transaction_id = models.CharField(max_length=100, blank=True, default='')
    transaction_type =  models.CharField(max_length=100, blank=True, default='')
    item =  models.CharField(max_length=100, blank=True, default='')
    total_transactions = models.CharField(max_length=100, blank=True, default='')
    request_id =  models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.transactions
    
   
    class Meta:
        ordering = ('accounts',)    