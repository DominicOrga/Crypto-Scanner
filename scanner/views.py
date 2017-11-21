from django.shortcuts import render
from django.http import JsonResponse
from libs.bittrexlib import bittrex
from . import utils as scannerutil

from .models import RsiModel

import datetime, time

TICK_INTERVAL = bittrex.TICKINTERVAL_FIVEMIN

def load_scanner(request):
	return render(request, "scanner/scanner.html")


def scan(request):
	table = []
	error = []

	btx = bittrex.Bittrex(bittrex.API_KEY, bittrex.API_SECRET, api_version = bittrex.API_V2_0)

	market_summaries = btx.get_market_summaries()

	if not market_summaries["success"]:
		error = ["Failed to acquire market summaries"]
		render(request, "scanner/scanner.html", { "error": error })

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
		price_change = (last - prevDay) / prevDay 
		market_name = summary["MarketName"]

		rsi = 0
		# candles = btx.get_candles(market_name, TICK_INTERVAL)

		# if (candles["success"]):
		# 	# time of last candle
		# 	t = time.strptime(candles["result"][-1]["T"], "%Y-%m-%dT%H:%M:%S")
		# 	last_candle_dt = datetime.datetime.fromtimestamp(time.mktime(t)) 

		# 	if request.GET["isRescan"] == "true":

		# 		try:
		# 			r = RsiModel.objects.get(market = market_name, datetime = last_candle_dt)
		# 			rs = r.ave_gain / r.ave_loss
		# 			rsi = 100 - 100 / (1 + rs)

		# 		except RsiModel.DoesNotExist:
		# 			last_candle_price = candles["result"][-1]["L"]
		# 			prec_candle_price = candles["result"][-2]["L"]

		# 			chg = last_candle_price - prec_candle_price

		# 			RsiModel.objects.get(market_name = market_name, datetime = )

		# 			r = RsiModel(market = market_name, ave_gain = ave_gain, ave_loss = ave_loss, datetime = last_candle_dt)
		# 			r.save()			

		# 	else:
		# 		last_prices = [c["L"] for c in candles["result"]]

		# 		ave_gain, ave_loss, rsi = scannerutil.rsi(last_prices)

		# 		try:
		# 			r = RsiModel.objects.get(market = market_name, datetime = last_candle_dt)
		# 		except RsiModel.DoesNotExist:
		# 			r = RsiModel(market = market_name, ave_gain = ave_gain, ave_loss = ave_loss, datetime = last_candle_dt)
		#			r.save()

		row_data = {
			"MarketName": market_name,
			"BaseVolume": "{:.3f}".format(summary["BaseVolume"]),
			"Bid":		  "{:.8f}".format(summary["Bid"]),
			"Ask": 		  "{:.8f}".format(summary["Ask"]),
			"Last": 	  "{:.8f}".format(last),
			"PrevDay": 	  "{:.8f}".format(prevDay),
			"Change": 	  "{:.1f}%".format(price_change * 100),
			"RSI":		  "{:.2f}".format(rsi)
		}

		table.append(row_data)

	return JsonResponse({'table': table})

