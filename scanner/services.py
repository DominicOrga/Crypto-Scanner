import threading
import time
from libs.bittrexlib import bittrex
from .models import RsiModel, MarketModel, MarketGroupModel
from . import utils as scannerutil

class MarketUpdate(object):
	__instance = None
	__is_running = False

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = object.__new__(cls)

		return cls.__instance

	def run(self):
		if (self.__is_running):
			return

		def daemon():
			rescan = False
			while True:
				self.scan(rescan = rescan)
				rescan = True
				time.sleep(10)

		th = threading.Thread(target = daemon)
		th.daemon = True
		th.start()

		self.__is_running = True

	def scan(self, rescan = False):

		btx = bittrex.Bittrex(bittrex.API_KEY, bittrex.API_SECRET, api_version = bittrex.API_V2_0)

		market_summaries = btx.get_market_summaries()

		if not market_summaries["success"]:
			return

		table = []

		# Filter markets
		markets = market_summaries["result"]
		markets = [ms for ms in markets 
					if ms["Market"]["BaseCurrency"] == "BTC" and 
					ms["Summary"]["PrevDay"] >= 0.01 and 
					ms["Summary"]["BaseVolume"] >= 750]
		markets = sorted(markets, key = lambda x: x["Summary"]["BaseVolume"], reverse = True)

		for ms in markets:
			summary = ms["Summary"]

			last = summary["Last"]
			prevDay = summary["PrevDay"]
			price_chg_24 = (last - prevDay) / prevDay 
			market_name = summary["MarketName"]

			price_chg_12 = 0
			price_chg_6 = 0
			candles = btx.get_candles(market_name, bittrex.TICKINTERVAL_HOUR)
			if (candles["success"]):
				# Not 12 or 6 because the other hour is attributed to the current price
				price_chg_12 = (last - candles["result"][-11]["L"]) / candles["result"][-11]["L"] 
				price_chg_6 = (last - candles["result"][-5]["L"]) / candles["result"][-5]["L"]

			rsi = 0
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

		marketgroup = MarketGroupModel.objects.create()
		marketgroup.markets.set(table)