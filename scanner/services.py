import threading
import time
import datetime
from libs.bittrexlib import bittrex
from .models import RsiModel, MarketModel, MarketGroupModel
from . import utils as scannerutil

class MarketUpdate(object):
	""" Service to gather market data from bittrex and coinmarketcap.
		
		A singleton service executed every second to gather raw market data, which is 
		then processed to output a filtered set of market data.

		Console Logs:
			Service Market Update Initialized: Displayed when the service starts.
			Service Market Update Executed:    Displayed when the service is executed every 
											   after one second.
			Service Market Update Finished:	   Displayed when the service execution ends.
	"""

	__instance = None
	__is_running = False

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = object.__new__(cls)

		return cls.__instance

	def run(self):
		if (self.__is_running):
			return

		print("Service Market Update Initialized...")

		def daemon():
			rescan = False
			while True:
				print("Service Market Update Executed...")
				self.scan(rescan = rescan)
				rescan = True
				print("Service Market Update Finished...")
				time.sleep(1)

		th = threading.Thread(target = daemon)
		th.daemon = True
		th.start()

		self.__is_running = True

	def scan(self, rescan = False):

		st = datetime.datetime.utcnow()

		btx = bittrex.Bittrex(bittrex.API_KEY, bittrex.API_SECRET, api_version = bittrex.API_V2_0)

		market_summaries = btx.get_market_summaries()

		if not market_summaries["success"]:
			return

		table = []

		""" Filter markets """
		markets = market_summaries["result"]
		markets = [ms for ms in markets 
					if ms["Market"]["BaseCurrency"] == "BTC" and 
					ms["Summary"]["PrevDay"] >= 0.01 and 
					ms["Summary"]["BaseVolume"] >= 750]
		markets = sorted(markets, key = lambda x: x["Summary"]["BaseVolume"], reverse = True)

		for ms in markets:
			pass
			summary = ms["Summary"]

			last = summary["Last"]
			prevDay = summary["PrevDay"]
			price_chg_24 = (last - prevDay) / prevDay 
			market_name = summary["MarketName"]

			price_chg_12 = 0
			price_chg_6 = 0
			candles = btx.get_candles(market_name, bittrex.TICKINTERVAL_HOUR)

			if (candles["success"]):
				""" Not 12 or 6 because the other hour is attributed to the current price """
				price_chg_12 = (last - candles["result"][-11]["L"]) / candles["result"][-11]["L"] 
				price_chg_6 = (last - candles["result"][-5]["L"]) / candles["result"][-5]["L"]

			last_rsi = 0
			candles = btx.get_candles(market_name, bittrex.TICKINTERVAL_ONEMIN)

			if (candles["success"]):
				candles_reduced = candles["result"][-250 : len(candles["result"])]
				last_candle_dt = scannerutil.btxdt_to_pydt(candles_reduced[-1]["T"])

				if rescan:
					try:
						p = RsiModel.objects.get(market = market_name, datetime = last_candle_dt)

						price_chg = last - candles_reduced[-1]["L"]
						last_ave_gain, last_ave_loss, last_rsi = scannerutil.update_rsi(p.ave_gain, p.ave_loss, price_chg)

					except RsiModel.DoesNotExist:
						candle_last_prices = [c["L"] for c in candles_reduced]
						ave_gain, ave_loss, rsi = scannerutil.rsi(candle_last_prices)

						price_chg = last - candle_last_prices[-1]
						last_ave_gain, last_ave_loss, last_rsi = scannerutil.update_rsi(ave_gain, ave_loss, price_chg)

						try:
							RsiModel.objects.get(market = market_name, datetime = last_candle_dt)
						except RsiModel.DoesNotExist:
							RsiModel.objects.create(market = market_name, ave_gain = ave_gain, ave_loss = ave_loss, datetime = last_candle_dt)

				else:
					candle_last_prices = [c["L"] for c in candles_reduced]
					ave_gain, ave_loss, rsi = scannerutil.rsi(candle_last_prices)

					price_chg = last - candle_last_prices[-1]
					last_ave_gain, last_ave_loss, last_rsi = scannerutil.update_rsi(ave_gain, ave_loss, price_chg)

					try:
						RsiModel.objects.get(market = market_name, datetime = last_candle_dt)
					except RsiModel.DoesNotExist:
						RsiModel.objects.create(market = market_name, ave_gain = ave_gain, ave_loss = ave_loss, datetime = last_candle_dt)

			m = MarketModel(
					market = market_name,
					base_volume = summary["BaseVolume"],
					bid = summary["Bid"],
					ask = summary["Ask"],
					last = last,
					previous_day = prevDay, 
					change_24h = price_chg_24,
					change_12h = price_chg_12,
					change_6h = price_chg_6,
					rsi = last_rsi)

			m.save()
			table.append(m)

		ft = datetime.datetime.utcnow() - st
		marketgroup = MarketGroupModel.objects.create(creation_delay_ms = scannerutil.deltatime_millis(ft))
		marketgroup.markets.set(table)

class MarketGroupModelCleanup(object):
	""" Service to delete Market Group Model records older than 15 days. """

	__instance = None
	__is_running = False

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = object.__new__(cls)

		return cls.__instance

	def run(self):
		if (self.__is_running):
			return

		print("Service Market Group Model Cleanup Initialized...")

		def daemon():
			rescan = False
			while True:
				print("Service Market Group Model Cleanup Executed...")
				self.clean()
				rescan = True
				print("Service Market Group Model Cleanup Finished...")
				 
				""" Sleep for one day """
				time.sleep(86400)

		th = threading.Thread(target = daemon)
		th.daemon = True
		th.start()

		self.__is_running = True

	def clean(self):
		dt_now = datetime.datetime.utcnow() 
		dt_last_month = dt_now - datetime.timedelta(15)

		try:
			res = MarketGroupModel.objects.filter(datetime_created__lt = dt_last_month)
			res.delete()
		except MarketGroupModel.DoesNotExist:
			pass