from django.shortcuts import render
import sys
from django.template.loader import get_template
from django.http import HttpResponse

# Create your views here.
def index(request):
 	
	t = get_template('index_test_2.html')
	html = t.render()

	return HttpResponse(html)

	# return render(request, "trading_app/index_test.html")

