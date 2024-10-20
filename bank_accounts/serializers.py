# bank_accounts/serializers.py

from rest_framework import serializers
from core.models import BankAccount
from django.contrib.auth import get_user_model
class BankAccountSerializer(serializers.ModelSerializer):
    user = (serializers.PrimaryKeyRelatedField(
            queryset=get_user_model().objects.all()))

    class Meta:
        model = BankAccount
        fields = [
            'account_number',   # This field will be writable
             # These fields will be read-only
            'user',
            'date_opened',
            'balance',
            'status',
            'account_type',
            'currency',
            'overdraft_limit',
        ]
        read_only_fields = [
             'user', 'date_opened', 'balance', 'status', 'account_type', 'currency', 'overdraft_limit'
        ]

    def create(self, validated_data):

        return super().create(validated_data)
