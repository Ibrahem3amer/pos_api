from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth import get_user_model
from pos.models import *

User = get_user_model()

class ReceiptListAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f') 
        self.shop = Shop.objects.create(name='Big Shop')
        r = Receipt.objects.create(
            name='new receipt',
            shop=self.shop,
            user=self.user
        )

    def test_get_all_receipts(self):
        """ Retrieve all 3 receipts created in db with self.user."""

        # Setup test
        r2 = Receipt.objects.create(
            name='new receipt',
            shop=self.shop,
            user=self.user
        )
        r3 = Receipt.objects.create(
            name='new receipt',
            shop=self.shop,
            user=self.user
        )
        
        # Exercise test
        url = reverse('api_receipts_list')
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.get(url)

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertTrue(len(request.data) == 3)

    def test_get_no_receipts(self):
        """ Returns [] due to empty receipts."""

        # Setup test
        Receipt.objects.all().delete()
        
        # Exercise test
        url = reverse('api_receipts_list')
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.get(url)

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertTrue(request.data == [])

    def test_post_new_receipts(self):
        """ increases number of receipts in db to 2."""

        # Setup test
        data = {
            'name': 'receipt',
            'user': self.user.id,
            'shop': self.shop.id
        }
        
        # Exercise test
        url = reverse('api_receipts_list')
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.post(url, data)

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_post_new_receipts_with_incorrect_user_and_shop(self):
        """ increases number of receipts in db to 2."""

        # Setup test
        data = {
            'name': 'receipt',
            'user': 999,
            'shop': 999
        }
        
        # Exercise test
        url = reverse('api_receipts_list')
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.post(url, data)

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)


class ReceiptInstanceAPITest(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f') 
        self.shop = Shop.objects.create(name='Big Shop')


    def test_get_non_existing_instance(self):
        """ Returns 404 not found."""

        # Setup test
        # Exercise test
        url = reverse('api_receipts_instance', kwargs={'receipt_id': 999})
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.get(url)

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_instance(self):
        """ Retrieve receipt with id=1."""

        # Setup test
        r2 = Receipt.objects.create(
            name='new receipt',
            shop=self.shop,
            user=self.user
        )

        # Exercise test
        url = reverse('api_receipts_instance', kwargs={'receipt_id': r2.id})
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.get(url, )

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(r2.id, request.data['id'])


    def test_update_given_instance(self):
        """ Change name of instance from new receipt to updated receipt."""

        # Setup test
        r2 = Receipt.objects.create(
            name='new receipt',
            shop=self.shop,
            user=self.user
        )
        data = {'name': 'updated receipt'}

        # Exercise test
        url = reverse('api_receipts_instance', kwargs={'receipt_id': r2.id})
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.put(url, data)

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertNotEqual(r2.name, request.data['name'])


    def test_delete_given_instance(self):
        """ Returns 402."""

        # Setup test
        r2 = Receipt.objects.create(
            name='new receipt',
            shop=self.shop,
            user=self.user
        )

        # Exercise test
        url = reverse('api_receipts_instance', kwargs={'receipt_id': r2.id})
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.delete(url)

        # Assert test
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)