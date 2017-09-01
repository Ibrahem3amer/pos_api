from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from pos.serializers import *
from pos.models import *


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def receipts_list(request, format=None):
    """ Receipts list associated with auth user."""

    if request.method == 'GET':
        # Retrieve all receipts that owned by user.
        try:
            receipts = Receipt.objects.filter(user=request.user)
            receipts_serialized = ReceiptSerializer(receipts, many = True)
            return Response(receipts_serialized.data)
        except:
            request.user.receipts = []
            return Response([])

    if request.method == 'POST':
        # Insert new receipt.
        receipt_instance = ReceiptPOSTSerializer(data=request.data)
        if receipt_instance.is_valid():
            receipt_instance.save()
            return Response(receipt_instance.data, status=status.HTTP_201_CREATED)
        return Response(receipt_instance.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def receipt_instance(request, receipt_id, format=None):
    """ Allows for Retreive, Update, Delete."""

    try:
        receipt = Receipt.objects.get(pk=receipt_id)
    except Receipt.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReceiptSerializer(receipt)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReceiptPOSTSerializer(receipt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def receipt_avg(request, receipt_id, format = None):
    """ Returns average of receipt's items."""

    try:
        receipt = Receipt.objects.get(pk=receipt_id)
        return Response({'average': receipt.get_avg()})
    except Receipt.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def pay_receipt(request, receipt_id, format = None):
    """ Pays receipt total cost."""

    try:
        receipt = Receipt.objects.get(pk=receipt_id)
        money = request.POST.get('money', -1)
        if receipt.pay_receipt(float(money)):
            return Response(status=status.HTTP_200_OK)        
    except Receipt.DoesNotExist:
        pass

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def items_list(request, receipt_id=0, format=None):
    """ All items available or some related to receipt_id."""

    if request.method == 'GET':
        # Retrieve all receipts that owned by user.
        if receipt_id:
            items = Item.objects.filter(receipt=receipt_id)
        else:
            items = Item.objects.all()
        items_serialized = ItemSerializer(items, many = True)
        return Response(items_serialized.data)


    if request.method == 'POST':
        # Insert new item.
        item_instance = ItemPOSTSerializer(data=request.data)
        if item_instance.is_valid():
            item_instance.save()
            return Response(item_instance.data, status=status.HTTP_201_CREATED)
        return Response(item_instance.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def item_instance(request, item_id, format=None):
    """ Allows for Retreive, Update, Delete."""

    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ItemPOSTSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def set_stock(request, item_id, format = None):
    """ Override the current stock amount of given item."""

    try:
        item = Item.objects.get(pk=item_id)
        amount = request.POST.get('amount', -1)
        item.set_stock_amount(amount)
        return Response(status=status.HTTP_200_OK)        
    except Item.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_most_sold(request, format = None):
    """ Returns the most sold item(s)."""

    items = Item.get_most_sold()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)