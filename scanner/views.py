from django.shortcuts import render
from libs.bittrexlib import bittrex


# Create your views here.
def scan(request):
	btx = bittrex.Bittrex(bittrex.API_KEY, bittrex.API_SECRET, api_version = bittrex.API_V2_0)

	market_summaries = btx.get_market_summaries()

	if not market_summaries["success"]:
		error = ["Failed to acquire market summaries"]
		render(request, "scanner/scanner.html", { "error": error })

	table = []

	results = market_summaries["result"]

	for i, ms in enumerate(results):

		market = ms["Market"]

		if market['BaseCurrency'] != 'BTC':
			continue

		summary = ms["Summary"]

		last = summary["Last"]
		prevDay = summary["PrevDay"]

		price_change = (last - prevDay) / prevDay 

		row_data = {}

		row_data["MarketName"] = summary["MarketName"]
		row_data["BaseVolume"] = "{:.3f}".format(summary["BaseVolume"])
		row_data["Bid"] = "{:.8f}".format(summary["Bid"])
		row_data["Ask"] = "{:.8f}".format(summary["Ask"])
		row_data["Last"] = "{:.8f}".format(last)
		row_data["PrevDay"] = "{:.8f}".format(prevDay)
		row_data["Change"] = "{:.1f}%".format(price_change * 100)

		table.append(row_data)

	return render(request, "scanner/scanner.html", { "table": table })
