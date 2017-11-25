from django.test import TestCase
from django.db.models.query import QuerySet
from libs.bittrexlib import bittrex
from scanner import utils as scanner
from scanner.models import RsiModel, MarketModel, MarketGroupModel

import datetime
import time
# Create your tests here.

class UtilTest(TestCase):

	def test_rsi(self):
		close_prices = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 
						46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46, 46.03, 46.41, 46.22, 
						45.64, 46.21]

		a, b, c = scanner.rsi(close_prices)
		self.assertTrue(abs(c - 62.93) < 1)

		a, b, c = scanner.update_rsi(a, b, 46.25 - close_prices[-1])
		self.assertTrue(abs(c - 63.26) < 1)

		a, b, c = scanner.update_rsi(a, b, 45.71 - 46.25)
		self.assertTrue(abs(c - 56.06) < 1)

		a, b, c = scanner.update_rsi(a, b, 46.45 - 45.71)
		self.assertTrue(abs(c - 62.38) < 1)

class RsiModelTest(TestCase):

	def test_datetime_manipulation(self):

		# dt = datetime.datetime(2012, 2, 3, 4, 4, 3) # Y m d H M S
		# OR making use of the string datetime acquired from bittrex json
		# CREATE
		dt = scanner.btxdt_to_pydt("2012-02-03T04:04:03")

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

		for i in range(300):
			dt = datetime.datetime(2012, 2, 3, 4, 4, 3) # Y m d H M S
			p = RsiModel(market = "BTC-ETH", ave_gain = 32, ave_loss = 0, datetime = dt)
			p.save()

		self.assertEquals(RsiModel.objects.all().count(), 200)		

		# populate original records
		RsiModel.objects.all().delete()
		RsiModel.objects.bulk_create(b)

		self.assertEquals(RsiModel.objects.all().count(), len(b))

class MarketGroupModelTest(TestCase):

	def test_delete_cascade(self):
		market_copy = list(MarketModel.objects.all())
		marketgroup_copy = list(MarketGroupModel.objects.all())

		MarketModel.objects.all().delete()
		MarketGroupModel.objects.all().delete()

		self.assertEquals(MarketModel.objects.all().count(), 0)
		self.assertEquals(MarketGroupModel.objects.all().count(), 0)

		mg = MarketGroupModel.objects.create()

		for i in range(5):
			m = MarketModel.objects.create(market="BTC-ETH", base_volume=1, bid=1, ask=1, last=1, previous_day=1, change_24h=1, change_12h=1, change_6h=1, rsi=1)
			mg.markets.add(m)

		self.assertEquals(MarketGroupModel.objects.all().count(), 1)
		self.assertEquals(MarketModel.objects.all().count(), 5)

		mg.delete()

		self.assertEquals(MarketGroupModel.objects.all().count(), 0)
		self.assertEquals(MarketModel.objects.all().count(), 0)

		MarketModel.objects.bulk_create(market_copy)
		MarketGroupModel.objects.bulk_create(marketgroup_copy)

		self.assertEquals(MarketModel.objects.all().count(), len(market_copy))
		self.assertEquals(MarketGroupModel.objects.all().count(), len(marketgroup_copy))