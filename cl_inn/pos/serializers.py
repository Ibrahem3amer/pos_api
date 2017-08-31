from rest_framework import serializers
from pos.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = User
        fields  = ('id', 'username', 'email', 'password')


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ('__all__')


class ReceiptSerializer(serializers.ModelSerializer):

    shop = ShopSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Receipt
        fields = ('__all__')


class ItemSerializer(serializers.ModelSerializer):

    receipt = ReceiptSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ('__all__')