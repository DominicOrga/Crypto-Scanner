from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from scanner.models import MarketModel
# Create your views here.
def load_strata(request):
	return render(request, "strata/strata.html")

def strata_markets(request):

	try:
		markets = MarketModel.objects.filter(rsi__lte = 25, change_24h__gte = 0.05, change_12h__gte = 0.025, change_6h__gte = 0)
		markets_dict = [model_to_dict(m) for m in markets]

		return JsonResponse({ "markets": markets_dict })

	except MarketModel.DoesNotExist:
		return JsonResponse({ "markets": "" })
		