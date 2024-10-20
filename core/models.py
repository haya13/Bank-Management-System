"""
Models for our system
"""

from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from bank_api import settings



class UserManager(BaseUserManager):
    """ Manager for the Users in the system"""

    def create_user(self, userId, email, password="12345", **extra_fields):
        """Creates and saves a new user"""
        if not userId:
            raise ValueError("Must provide a userId")
        if not email:
            raise ValueError("Must provide an email address")

        email = self.normalize_email(email)
        user = self.model(userId=userId, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, userId, email, password="12345"):
        """Creates a superuser"""
        user = self.create_user(userId=userId, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255)
    userId = models.CharField(max_length=255,unique=True,default='default_user_id')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = ['email']


class BankAccount(models.Model):
    ACCOUNT_TYPES = [
        ('individual', 'Individual'),
        ('shared', 'Shared'),
    ]

    CURRENCIES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('JRD', 'Jordanian Dinar'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
    ]

    account_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Ensure to hash password securely
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
       )
    date_opened = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2 ,default=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES , default='individual')
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='USD')
    overdraft_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return (
            f"Account Number: {self.account_number}, "
            f"User: {self.user.id if self.user else 'None'}, "
            f"Date Opened: {self.date_opened}, "
            f"Balance: {self.balance}, "
            f"Status: {self.status}, "
            f"Account Type: {self.account_type}, "
            f"Currency: {self.currency}, "
            f"Overdraft Limit: {self.overdraft_limit}"
        )


class Transaction(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
    timestamp = models.DateTimeField(auto_now_add=True)

