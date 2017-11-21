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

		candles = btx.get_candles(market_name, TICK_INTERVAL)
		if (candles["success"]):
			if request.GET["isRescan"] == "true":
				last_candle = candles["result"][-1]

				last_candle_dt = scannerutil.btxdt_to_pydt(last_candle["T"])

				try:
					r = RsiModel.objects.get(market = market_name, datetime = last_candle_dt)
					rs = r.ave_gain / r.ave_loss
					rsi = 100 - 100 / (1 + rs)

				except RsiModel.DoesNotExist:
					prec_candle = candles["result"][-2]
					prec_candle_dt = scannerutil.btxdt_to_pydt(prec_candle["T"])

					chg = last_candle["L"] - prec_candle["L"]

					last_rsi = RsiModel.objects.get(market = market_name, datetime = prec_candle_dt)

					ave_gain, ave_loss, rsi = scannerutil.update_rsi(last_rsi.ave_gain, last_rsi.ave_loss, chg)

					r = RsiModel(market = market_name, ave_gain = ave_gain, ave_loss = ave_loss, datetime = last_candle_dt)
					r.save()

			else:
				last_prices = [c["L"] for c in candles["result"]]
				ave_gain, ave_loss, rsi = scannerutil.rsi(last_prices)

				last_candle_dt = scannerutil.btxdt_to_pydt(candles["result"][-1]["T"])
				try:
					r = RsiModel.objects.get(market = market_name, datetime = last_candle_dt)
				except RsiModel.DoesNotExist:
					r = RsiModel(market = market_name, ave_gain = ave_gain, ave_loss = ave_loss, datetime = last_candle_dt)
					r.save()

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

