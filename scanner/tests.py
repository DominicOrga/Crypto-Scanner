from django.test import TestCase
from libs.bittrexlib import bittrex
from scanner import utils as scanner
from scanner.models import RsiModel
import datetime
# Create your tests here.

class UtilTest(TestCase):

	def test_rsi(self):
		close_prices = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 
						46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46, 46.03, 46.41, 46.22, 
						45.64, 46.21]

		a, b, c = scanner.rsi(close_prices)

		self.assertTrue(c - 63.93 < 0.01)

class RsiModelTest(TestCase):

	def test_datetime_insertion(self):

		a = RsiModel.objects.all().count()

		p = RsiModel(ave_gain=32, ave_loss=0, datetime="2012-2-3 4:4:3")
		p.save()

		self.assertEquals(RsiModel.objects.all().count(), a + 1)

		RsiModel.objects.last().delete()
		self.assertEquals(RsiModel.objects.all().count(), a)
