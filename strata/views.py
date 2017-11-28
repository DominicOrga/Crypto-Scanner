from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from scanner.models import MarketModel
import datetime

def load_strata(request):
	return render(request, "strata/strata.html")

def strata_markets(request):

	try:
		markets = MarketModel.objects.filter(rsi__lte = 25, change_24h__gte = 0.05, change_12h__gte = 0.025, change_6h__gte = 0)
		# markets = MarketModel.objects.filter(rsi__lte = 100) # Debugging purposes
		
		dt_now = datetime.datetime.utcnow()
		timedelta = datetime.timedelta(minutes=15)

		''' Add is_recent field and datetime_formatted in market models '''
		markets_dict = [
			dict(model_to_dict(m), 
				datetime_formatted = m.datetime_created.strftime("%b-%d-%Y, %H:%M:%S"), 
				is_recent = (timedelta - (dt_now - m.datetime_created.replace(tzinfo=None))).days >= 0) 
			for m in markets]

		markets_dict_sorted = sorted(markets_dict, key = lambda k: k["datetime_created"], reverse = True)

		return JsonResponse({ "markets": markets_dict_sorted })

	except MarketModel.DoesNotExist:
		return JsonResponse({ "markets": [] })
		