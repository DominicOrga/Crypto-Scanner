from django.shortcuts import render

# Create your views here.
def load_strata(request):
	return render(request, "strata/strata.html")