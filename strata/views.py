from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from scanner.models import MarketModel
import datetime

def load_strata(request):
	return render(request, "strata/strata.html")

def strata_markets(request):

	try:
		# expected: rsi__lte = 25. rsi__lte = 100 is used for debugging
		markets = MarketModel.objects.filter(rsi__lte = 100, change_24h__gte = 0.05, change_12h__gte = 0.025, change_6h__gte = 0)
		dt_now = datetime.datetime.utcnow()
		timedelta = datetime.timedelta(minutes=15)

		markets_dict = [dict(model_to_dict(m), is_recent = (timedelta - (dt_now - m.datetime_created.replace(tzinfo=None))).days >= 0) for m in markets]

		return JsonResponse({ "markets": markets_dict })

	except MarketModel.DoesNotExist:
		return None
		