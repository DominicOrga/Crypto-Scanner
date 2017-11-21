from django.test import TestCase
from django.db.models.query import QuerySet
from libs.bittrexlib import bittrex
from scanner import utils as scanner
from scanner.models import RsiModel

import datetime
import time
# Create your tests here.

class UtilTest(TestCase):

	def test_rsi(self):
		close_prices = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 
						46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46, 46.03, 46.41, 46.22, 
						45.64, 46.21]

		a, b, c = scanner.rsi(close_prices)

		self.assertTrue(c - 63.93 < 0.01)

class RsiModelTest(TestCase):

	def test_datetime_manipulation(self):

		# dt = datetime.datetime(2012, 2, 3, 4, 4, 3) # Y m d H M S
		# OR making use of the string datetime acquired from bittrex json
		# CREATE
		t = time.strptime("2012-02-03T04:04:03", "%Y-%m-%dT%H:%M:%S")
		dt = datetime.datetime.fromtimestamp(time.mktime(t))

		q = RsiModel.objects.filter(market = "BTC-ETH", datetime = dt)
		q.delete()		

		a = RsiModel.objects.all().count()

		p = RsiModel(market = "BTC-ETH", ave_gain = 32, ave_loss = 0, datetime = dt)
		p.save()

		self.assertEquals(RsiModel.objects.all().count(), a + 1)

		# READ
		dt2 = RsiModel.objects.get(market = "BTC-ETH", datetime = dt).datetime
		self.assertEquals(type(dt), type(dt2))

	def test_table_limit(self):

		b = list(RsiModel.objects.all()) # backup records
		c = len(b)

		for i in range(300):
			dt = datetime.datetime(2012, 2, 3, 4, 4, 3) # Y m d H M S
			p = RsiModel(market = "BTC-ETH", ave_gain = 32, ave_loss = 0, datetime = dt)
			p.save()

		self.assertEquals(RsiModel.objects.all().count(), 200)		

		# populate original records
		RsiModel.objects.all().delete()
		for i in range(len(b)):
			b[i].save()

		self.assertEquals(RsiModel.objects.all().count(), c)
