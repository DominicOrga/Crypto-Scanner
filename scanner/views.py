from django.shortcuts import render
from django.http import JsonResponse
from libs.bittrexlib import bittrex
from . import utils as scannerutil

from .models import RsiModel

import datetime, time

TICK_INTERVAL = bittrex.TICKINTERVAL_ONEMIN

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
		price_chg_24 = (last - prevDay) / prevDay 
		market_name = summary["MarketName"]

		price_chg_14 = 0
		candles = btx.get_candles(market_name, bittrex.TICKINTERVAL_HOUR)
		if (candles["success"]):
			# Not 13 because the other hour is attributed to the current price
			price_chg_14 = (last - candles["result"][-13]["L"]) / candles["result"][-13]["L"] 

		rsi = 0
		candles = btx.get_candles(market_name, bittrex.TICKINTERVAL_ONEMIN)
		if (candles["success"]):
			candles_reduced = candles["result"][-250 : len(candles["result"])]
			last_candle_dt = scannerutil.btxdt_to_pydt(candles_reduced[-1]["T"])

			if request.GET["isRescan"] == "true":
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

		row_data = {
			"MarketName": market_name,
			"BaseVolume": summary["BaseVolume"],
			"Bid":		  summary["Bid"],
			"Ask": 		  summary["Ask"],
			"Last": 	  last,
			"PrevDay": 	  prevDay,
			"Change24Hr": price_chg_24,
			"Change14Hr": price_chg_14,
			"RSI":		  last_rsi
		}

		table.append(row_data)

	return JsonResponse({'table': table})

