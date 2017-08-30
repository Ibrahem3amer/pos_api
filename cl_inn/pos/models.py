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
    stock_amount = models.IntegerField(
        validators=[MinLengthValidator(0, stock_amount_msg)]
    )
    shop = models.ForeignKey(
        'Shop',
        related_name='items',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'users.User',
        related_name='items',
        on_delete=models.CASCADE
    )
    cashier = models.IntegerField(default=-1) # Can be updated in future.


