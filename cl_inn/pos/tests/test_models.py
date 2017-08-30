from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve
from django.core.exceptions import ValidationError
from unittest import skip
from pos.models import Shop, Receipt, Item

User = get_user_model()

class ReceiptTest(TestCase):

	def setUp(self):
		self.shop = Shop.objects.create(name='Big Shop')
		self.user = User.objects.create_user(username='Ibrahem', password='010d1d5ss57cxs1x0d')
		self.name = 'Big new item'
		self.paid_amount = 1000

	def test_name_with_normal_chars(self):
		""" Saves item instance with proper name."""
		
		# Setup test
		r = Receipt.objects.create(
			name=self.name,
			paid_amount=self.paid_amount,
			shop=self.shop,
			user=self.user
		)

		# Exercise test
		receipts_in_db = Receipt.objects.all().count()

		# Assert test
		self.assertEqual(None, r.full_clean())
		self.assertTrue(receipts_in_db > 0)

	def test_numbers_in_start_of_name(self):
		""" Yales that name cannot be saved."""
		
		# Setup test
		self.name = '12345name'
		r = Receipt.objects.create(
			name=self.name,
			paid_amount=self.paid_amount,
			shop=self.shop,
			user=self.user
		)

		# Exercise test
		receipts_in_db = Receipt.objects.all().count()

		# Assert test
		with self.assertRaisesRegexp(ValidationError, 'Name cannot start with number, should consist of characters.'):
			r.full_clean()

	def test_pays_negative_sum(self):
		""" Yales that money cannot be negative."""
		
		# Setup test
		r = Receipt.objects.create(
			name=self.name,
			paid_amount=-100,
			shop=self.shop,
			user=self.user
		)

		# Exercise test
		receipts_in_db = Receipt.objects.all().count()

		# Assert test
		with self.assertRaisesRegexp(ValidationError, 'Money cannot be negative!'):
			r.full_clean()


