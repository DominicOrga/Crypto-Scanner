from django.test import TestCase
from libs.bittrexlib import bittrex
from scanner import utils as scanner
# Create your tests here.

def test_get_candles():

	btx = bittrex.Bittrex(bittrex.API_KEY, bittrex.API_SECRET, api_version = bittrex.API_V2_0)

	candles = btx.get_candles("BTC-ETH", bittrex.TICKINTERVAL_HOUR)

	print(candles["result"][-1]["T"])

def test_rsi():
	close_prices = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 
					46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46, 46.03, 46.41, 46.22, 
					45.64, 46.21]

	a, b, c = scanner.rsi(close_prices)

	print(c)