import copy

from rest_framework import serializers
from transplaid.models import Transaction, InitialPullTransaction


class LocationSerializer(serializers.Serializer):
    lat = serializers.CharField(allow_null=True, default="")
    city = serializers.CharField(allow_null=True, default="")
    zip = serializers.CharField(allow_null=True, default="")
    store_number = serializers.CharField(allow_null=True, default="")
    state = serializers.CharField(allow_null=True, default="")
    lon = serializers.CharField(allow_null=True, default="")
    address = serializers.CharField(allow_null=True, default="")


class PaymentDataSerializer(serializers.Serializer):
   payment_method = serializers.CharField(allow_null=True, default="")
   reason = serializers.CharField(allow_null=True, default="")
   by_order_of = serializers.CharField(allow_null=True, default="")
   payee = serializers.CharField(allow_null=True, default="")
   ppd_id = serializers.CharField(allow_null=True, default="")
   reference_number = serializers.CharField(allow_null=True, default="")
   payment_processor = serializers.CharField(allow_null=True, default="")


class AbstractTransactionSerializer(serializers.Serializer):
    transaction_id = serializers.CharField()
    category_id = serializers.CharField(allow_null=True, default="")
    category = serializers.ListField(allow_null=True, default="")
    pending_transaction_id = serializers.CharField(allow_null=True, default="")
    transaction_type = serializers.CharField()
    name = serializers.CharField()
    amount = serializers.DecimalField(decimal_places=2, max_digits=None)
    date = serializers.DateField()
    account_id = serializers.CharField()
    account_owner = serializers.CharField(allow_null=True, default="")
    pending = serializers.BooleanField()
    
    location = LocationSerializer()
    payment_meta = PaymentDataSerializer()

    class Meta:
        abstract = True


class TransactionSerializer(AbstractTransactionSerializer):
    def create(self, validated_data):
        data = copy.copy(validated_data)
        result_data = {}
        try:
            result_data = data.pop('location')
            result_data.update(data.pop('payment_meta'))
        except KeyError:
            pass
        result_data.update(data)
        return Transaction.objects.create(**result_data)


class InitialPullTransactionSerializer(AbstractTransactionSerializer):
    def create(self, validated_data):
        data = copy.copy(validated_data)
        result_data = {}        
        try:
            result_data = data.pop('location')
            result_data.update(data.pop('payment_meta'))
        except KeyError:
            pass
        result_data.update(data)
        return InitialPullTransaction.objects.create(**result_data)
