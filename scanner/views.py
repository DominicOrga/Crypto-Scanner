from django.shortcuts import render
from libs.bittrexlib import bittrex



# Create your views here.
def scan(request):
	btx = bittrex.Bittrex()