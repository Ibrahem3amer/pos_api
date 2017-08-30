from django.urls import reverse
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.core.exceptions import ValidationError
from unittest import skip
from users import User
from pos import Shop, Item

class ItemTest(TestCase):

	def setUp(self):
		self.shop = Shop.objects.create('Big Shop')

	def test_name_with_normal_chars(self):
		""" Saves item instance with proper name."""
		
		# Setup test
		name = 'Big new item!'
		# Exercise test
		# Assert test