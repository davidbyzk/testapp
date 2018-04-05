from __future__ import unicode_literals
import datetime
from django.db import models
# from pygments.lexers import get_all_lexers
# from pygments.styles import get_all_styles
# from Lib.unittest.util import _MAX_LENGTH
# from pygments.lexers import get_lexer_by_name
# from pygments.formatters.html import HtmlFormatter
# from pygments import highlight
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
    created = models.DateTimeField(auto_created=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transaction', on_delete=models.CASCADE)
    account_id = models.CharField(max_length=100, blank=True, default='')
    amount = models.CharField(max_length=100, blank=True, default='')
    category = models.CharField(max_length=100, blank=True, default='', null=True)
    category_id = models.CharField(max_length=100, blank=True, default='', null=True)
    address = models.CharField(max_length=100, blank=True, default='', null=True)
    city = models.CharField(max_length=100, blank=True, default='', null=True)
    state = models.CharField(max_length=100, blank=True, default='', null=True)
    lat = models.CharField(max_length=100, blank=True, default='', null=True)
    lon = models.CharField(max_length=100, blank=True, default='', null=True)
    name = models.CharField(max_length=100, blank=True, default='')
    pending = models.CharField(max_length=100, blank=True, default='')
    pending_transaction_id = models.CharField(max_length=100, blank=True, default='', null=True)
    account_owner = models.CharField(max_length=100, blank=True, default='', null=True)
    transaction_id = models.CharField(max_length=100, blank=True, default='')
    transaction_type = models.CharField(max_length=100, blank=True, default='')
    item = models.CharField(max_length=100, blank=True, default='')
    request_id = models.CharField(max_length=100, blank=True, default='')
    payment_method = models.CharField(max_length=100, blank=True, default='', null=True)
    reason = models.CharField(max_length=100, blank=True, default='', null=True)
    by_order_of = models.CharField(max_length=100, blank=True, default='', null=True)
    payee = models.CharField(max_length=100, blank=True, default='', null=True)
    ppd_id = models.CharField(max_length=100, blank=True, default='', null=True)
    reference_number = models.CharField(max_length=100, blank=True, default='', null=True)
    payment_processor = models.CharField(max_length=100, blank=True, default='', null=True)
    date = models.DateField()
    zip = models.CharField(max_length=100, blank=True, default='', null=True)
    store_number = models.CharField(max_length=100, blank=True, default='', null=True)

    def __str__(self):
        return "Transaction %s" % self.transaction_id

    class Meta:
        ordering = ('transaction_id',)    
