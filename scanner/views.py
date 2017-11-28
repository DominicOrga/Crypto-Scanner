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

		market_group_dict = model_to_dict(market_group)
		market_group_dict['markets'] = [model_to_dict(m) for m in market_group.markets.all()]

		return JsonResponse({ "market_group": market_group_dict })

	except MarketGroupModel.DoesNotExist:
		JsonResponse({ "market_group": [] })

def last_market_update(request):
	try:
		market_group = MarketGroupModel.objects.last()
		dt = market_group.datetime_created
		
		return JsonResponse({ "datetime": dt.strftime("%b-%d-%Y, %H:%M:%S") })

	except MarketGroupModel.DoesNotExist:
		return JsonResponse({ "datetime": "" })