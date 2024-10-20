# bank_accounts/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import BankAccount
from bank_accounts.serializers import BankAccountSerializer
from rest_framework.decorators import action


class BankAccountViewSet(viewsets.ModelViewSet):
    """Manage bank accounts including creation and suspension."""
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Customize the creation process to associate the account with the authenticated user."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='suspend')
    def suspend_account(self, request):
        """Suspend a bank account."""
        account_number = request.data.get('account_number')
        print(f"Received request to suspend account number: {account_number}")  # Debugging print

        try:
            # Debugging: Check if the user is authenticated
            print(f"Authenticated user: {request.user}")
            account = BankAccount.objects.get(account_number=account_number, user=request.user)  # Check user ownership

            # Debugging: Output the current status of the account
            print(f"Current account status: {account.status}")

            if account.status == 'suspended':
                print("Account is already suspended.")
                return Response({"detail": "Account is already suspended."}, status=409)  # 409 Conflict

            account.status = 'suspended'
            account.save(update_fields=['status'])  # Update only the status field
            print(f"Account suspended successfully: {account}")  # Debugging print
            return Response({"detail": "Account suspended successfully."}, status=200)

        except BankAccount.DoesNotExist:
            print(f"Account not found for account number: {account_number}")  # Debugging print
            return Response({"detail": "Account not found or you do not own this account."}, status=404)

