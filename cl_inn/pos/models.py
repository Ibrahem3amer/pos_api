from django.db import models
from pos import validators as custom_validators
from django.core.validators import MinLengthValidator

# Create your models here.
class Shop(models.Model):

    # Attributes
    name = models.CharField(
        max_length=255,
        validators=[custom_validators.GeneralCMSValidator.name_validator]
    )
    is_active = models.BooleanField(default=True)


class Receipt(models.Model):
    
    # Helpers
    paid_msg = 'Money cannot be negative!'

    # Attributes 
    name = models.CharField(
        max_length=255,
        validators=[custom_validators.GeneralCMSValidator.name_validator]
    )
    date = models.DateTimeField(auto_now=True)
    total_amount = models.FloatField()
    paid_amount = models.FloatField(validators=[MinLengthValidator(0, paid_msg)])
    user = models.ForeignKey(
        'users.User',
        related_name='items',
        on_delete=models.CASCADE
    )
    shop = models.ForeignKey(
        'Shop',
        related_name='receipts',
        on_delete=models.CASCADE
    )
    cashier = models.IntegerField(default=-1) # Can be updated in future.


class Item(models.Model):

    # Helpers
    price_msg = 'Price cannot be negative!'
    stock_amount_msg = 'Stock is empty!'

    # Attributes
    code = models.CharField(max_length=255)
    name = models.CharField(
        max_length=255,
        validators=[custom_validators.GeneralCMSValidator.name_validator]
    )
    price = models.FloatField(validators=[MinLengthValidator(0, price_msg)])
    discount = models.FloatField(validators=[MinLengthValidator(0, price_msg)], default=0)
    stock_amount = models.IntegerField(
        validators=[MinLengthValidator(0, stock_amount_msg)]
    )
    receipt = models.ForeignKey(
        'Receipt',
        related_name='items',
        on_delete=models.CASCADE
    )

    # Methods 
    @property
    def total_price(self):
        """ Returns the calculated total price after discount."""
        return self.price - (self.discount*self.price)


