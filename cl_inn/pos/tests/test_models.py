from django.urls import reverse
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.core.exceptions import ValidationError
from unittest import skip
from users import User

class ShopTest(TestCase):

	def setUp(self):
		