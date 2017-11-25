from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse
from libs.bittrexlib import bittrex
from . import utils as scannerutil

from .models import MarketModel, MarketGroupModel

import datetime, time

def load_scanner(request):
	return render(request, "scanner/scanner.html")


def scan(request):

	try:
		market_group = MarketGroupModel.objects.last()
		table = [model_to_dict(m) for m in market_group.markets.all()]
		return JsonResponse({'table': table})

	except MarketGroupModel.DoesNotExist:
		return JsonResponse({'table': market_group})