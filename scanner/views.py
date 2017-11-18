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

		s = ms["Summary"]

		last = s["Last"]
		prevDay = s["PrevDay"]

		price_change = (last - prevDay) / prevDay 

		row_data = []
		row_data.append(s["MarketName"])
		row_data.append("{:.8f}".format(s["Volume"]))
		row_data.append("{:.8f}".format(s["Bid"]))
		row_data.append("{:.8f}".format(s["Ask"]))
		row_data.append("{:.8f}".format(last))
		row_data.append("{:.8f}".format(prevDay))
		row_data.append("{:.2f}%".format(price_change * 100))

		table.append("<tr bgcolor={}>".format("Gainsboro" if i % 2 == 0 else "White"))
		for col in row_data:
			table.append("<td>")
			table.append(col)
			table.append("</td>")

		table.append("</tr>")

	table_str = "".join(table)
	return render(request, "scanner/scanner.html", { "table": table_str })
