from django.db import models
from pos import validators as custom_validators
from django.core.validators import MinValueValidator, MaxValueValidator

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
    paid_amount = models.FloatField(
        validators=[MinValueValidator(0, paid_msg)],
        default=0
    )
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

    # Methods
    @property
    def total_amount(self):
        """ Sums all total prices of associated items."""
        items = Item.objects.filter(receipt=self)
        result = 0
        for item in items:
            result += item.total_price

        return result

    def pay_receipt(self, sum):
        """ Marks receipts as paid."""
        if (not self.paid_amount) and (sum == self.total_amount):
            self.paid_amount = float(sum)
            return True
        return False


class Item(models.Model):

    # Helpers
    price_msg = 'Price cannot be negative!'
    stock_amount_msg = 'Stock is empty!'
    discount_msg = 'Discount should be less than original price!'

    # Attributes
    code = models.CharField(max_length=255)
    name = models.CharField(
        max_length=255,
        validators=[custom_validators.GeneralCMSValidator.name_validator]
    )
    price = models.FloatField(
        validators=[MinValueValidator(0, price_msg)]
    )
    discount = models.FloatField(
        validators=[
            MinValueValidator(0, price_msg),
            MaxValueValidator(1, discount_msg)
        ],
        default=0
    )
    stock_amount = models.IntegerField(
        validators=[MinValueValidator(0, stock_amount_msg)],
        default=0
    )
    receipt = models.ForeignKey(
        'Receipt',
        related_name='items',
        on_delete=models.CASCADE
    )

    # Methods 
    @classmethod
    def get_most_sold(cls):
        """ Returns the most sold item."""
        target_amount = Item.objects.aggregate(target=models.Min('stock_amount'))
        items = Item.objects.filter(stock_amount=target_amount['target'])
        return items


    @property
    def total_price(self):
        """ Returns the calculated total price after discount."""
        return self.price - (self.discount*self.price)

    def decrease_stock(self, i=1):
        """ Decreases the item stock by i items."""
        if i <= self.stock_amount:
            self.stock_amount -= int(i)

    def set_stock_amount(self, amount=0):
        """ Set stock amount to given amount."""
        self.stock_amount = int(amount) if int(amount) >= 0 else self.stock_amount



