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

	def test_correct_total_amount(self):
		""" Returns the sum of total price for each item.
		>>> 300, 300, 300
		900
		"""
		
		# Setup test
		r = Receipt.objects.create(
			name=self.name,
			paid_amount=-100,
			shop=self.shop,
			user=self.user
		)

		# Exercise test
		for i in range(3):
			item = Item.objects.create(
				name='item',
				code='item'+str(i),
				price=300,
				discount=0,
				stock_amount=3,
				receipt=r
			)

		# Assert test
		self.assertEqual(r.total_amount, 900)

	def test_correct_total_amount_with_discounted_values(self):
		""" Returns the sum of total price for each item.
		>>> (100, 0.10), (2458, 1), (300, 0.05)
		375
		"""
		
		# Setup test
		r = Receipt.objects.create(
			name=self.name,
			paid_amount=-100,
			shop=self.shop,
			user=self.user
		)
		prices = [100, 2458, 300]
		discounts = [0.10, 1, 0.05]

		# Exercise test
		for i in range(3):
			item = Item.objects.create(
				name='item',
				code='item'+str(i),
				price=prices[i],
				discount=discounts[i],
				stock_amount=3,
				receipt=r
			)

		# Assert test
		self.assertEqual(r.total_amount, 375)

	def test_pay_receipt_with_positive_parameter_eq_amount(self):
		""" Returns true and updates paid_amount."""
		
		# Setup test
		r = Receipt.objects.create(
			name=self.name,
			shop=self.shop,
			user=self.user
		)
		for i in range(3):
			Item.objects.create(
				name='item',
				code='item'+str(i),
				price=300,
				discount=0,
				stock_amount=3,
				receipt=r
			)

		# Exercise test
		r.pay_receipt(900)


		# Assert test
		self.assertEqual(r.paid_amount, 900)

	def test_pay_receipt_with_positive_parameter_ls_amount(self):
		""" Returns true and updates paid_amount."""
		
		# Setup test
		r = Receipt.objects.create(
			name=self.name,
			shop=self.shop,
			user=self.user
		)
		for i in range(3):
			Item.objects.create(
				name='item',
				code='item'+str(i),
				price=300,
				discount=0,
				stock_amount=3,
				receipt=r
			)

		# Exercise test
		r.pay_receipt(400)


		# Assert test
		self.assertEqual(r.paid_amount, 0)


class ItemTest(TestCase):

	def setUp(self):
		self.shop = Shop.objects.create(name='Big Shop')
		self.user = User.objects.create_user(username='Ibrahem', password='010d1d5ss57cxs1x0d')
		self.name = 'Big new item'
		self.paid_amount = 1000
		self.receipt = Receipt.objects.create(
			name=self.name,
			paid_amount=self.paid_amount,
			shop=self.shop,
			user=self.user
		)
		self.code = '515ds1d5s1a231$%&FSas'
		self.itm_name = 'new one'
		self.price = 10
		self.stock_amount = 3

	def test_basic_item(self):
		""" Saves an item successfully."""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=self.price,
			stock_amount=self.stock_amount,
			receipt=self.receipt
		)

		# Exercise test
		itms_in_db = Item.objects.all().count()

		# Assert test
		self.assertEqual(None, item.full_clean())
		self.assertTrue(itms_in_db > 0)

	def test_negative_price(self):
		""" Yales that price cannot be negative."""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=-10,
			stock_amount=self.stock_amount,
			receipt=self.receipt
		)

		# Exercise test
		# Assert test
		with self.assertRaisesRegexp(ValidationError, 'Price cannot be negative!'):
			item.full_clean()

	def test_negative_stock_amount(self):
		""" Yales that stock is empty."""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=self.price,
			stock_amount=-1,
			receipt=self.receipt
		)

		# Exercise test
		# Assert test
		with self.assertRaisesRegexp(ValidationError, 'Stock is empty!'):
			item.full_clean()

	def test_total_amount(self):
		""" Returns correct price after discount.
		>>> price=300, discount=0.10
		270
		>>> price=25000, discount=0.07
		23250
		"""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=300,
			discount=0.10,
			stock_amount=self.stock_amount,
			receipt=self.receipt
		)
		item2 = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=25000,
			discount=0.07,
			stock_amount=self.stock_amount,
			receipt=self.receipt
		)

		# Exercise test
		# Assert test
		self.assertEqual(item2.total_price, 23250)

	def test_total_amount_with_negative_discount(self):
		""" Yales that discount cannot be negative."""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=300,
			discount=-0.10,
			stock_amount=self.stock_amount,
			receipt=self.receipt
		)
		# Exercise test
		# Assert test
		with self.assertRaisesRegexp(ValidationError, 'Price cannot be negative!'):
			item.full_clean()

	def test_total_amount_with_discount_gt_price(self):
		""" Yales that discount cannot be greater than price."""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=300,
			discount=3,
			stock_amount=self.stock_amount,
			receipt=self.receipt
		)
		# Exercise test
		# Assert test
		with self.assertRaisesRegexp(ValidationError, 'Discount should be less than original price!'):
			item.full_clean()

	def test_set_stock_amount(self):
		""" Changes item's stock_amount by i."""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=300,
			stock_amount=self.stock_amount,
			receipt=self.receipt
		)

		# Exercise test
		item.set_stock_amount(99)

		# Assert test
		self.assertNotEqual(item.stock_amount, self.stock_amount)
		self.assertEqual(item.stock_amount, 99)

	def test_set_stock_amount_with_negative(self):
		""" Doesn't change anything."""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=300,
			stock_amount=self.stock_amount,
			receipt=self.receipt
		)

		# Exercise test
		item.set_stock_amount(-99)

		# Assert test
		self.assertEqual(item.stock_amount, self.stock_amount)
		self.assertNotEqual(item.stock_amount, 99)

	def test_decrease_stock_with_no_parameter(self):
		""" Decreases stock amount by 1."""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=300,
			stock_amount=self.stock_amount,
			receipt=self.receipt
		)

		# Exercise test
		item.decrease_stock()

		# Assert test
		self.assertTrue(item.stock_amount < self.stock_amount)
		self.assertEqual(item.stock_amount, self.stock_amount-1)

	def test_decrease_stock_with_positive_parameter_ls_amount(self):
		""" Decreases stock amount by 5."""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=300,
			stock_amount=10,
			receipt=self.receipt
		)

		# Exercise test
		item.decrease_stock(5)

		# Assert test
		self.assertTrue(item.stock_amount < 10)
		self.assertEqual(item.stock_amount, 10-5)

	def test_decrease_stock_with_positive_parameter_gt_amount(self):
		""" Doesn't change anything."""
		
		# Setup test
		item = Item.objects.create(
			name=self.itm_name,
			code=self.code,
			price=300,
			stock_amount=self.stock_amount,
			receipt=self.receipt
		)

		# Exercise test
		item.decrease_stock(5)

		# Assert test
		self.assertEqual(item.stock_amount, self.stock_amount)

	def test_most_sold_item(self):
		""" Returns item with stock_amount = 1."""
		
		# Setup test
		prices = [100, 2458, 300]
		stock = [10, 1, 35]

		# Exercise test
		for i in range(3):
			Item.objects.create(
				name='item',
				code='item'+str(i),
				price=prices[i],
				stock_amount=stock[i],
				receipt=self.receipt
			)

		# Assert test
		self.assertEqual(Item.get_most_sold().first().stock_amount, 1)

	def test_most_sold_item_when_no_items(self):
		""" Returns None."""
		
		# Setup test
		# Assert test
		self.assertEqual(Item.get_most_sold().first(), None)

