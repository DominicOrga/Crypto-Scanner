from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.mail import send_mass_mail
from django.conf import settings
from scanner.models import MarketModel, SubscriptionModel
import datetime

def load_strata(request):
	return render(request, "strata/strata.html")

def strata_markets(request):

	def duration(datetime_now, datetime_created):
		delta = datetime_now - datetime_created

		m = int(delta.seconds / 60)
		s = delta.seconds - m * 60

		return str(m) + "m " + str(s) + "s ago"

	try:
		markets = MarketModel.objects.filter(rsi__lte = 25, change_24h__gte = 0.05, change_12h__gte = 0.025, change_6h__gte = 0).order_by("-datetime_created")
		# markets = MarketModel.objects.filter(rsi__lte = 100) # Debugging purposes

		dt_now = datetime.datetime.utcnow()
		timedelta = datetime.timedelta(minutes=15)

		''' Add is_recent field and datetime_formatted in market models '''
		markets_dict = [
			dict(model_to_dict(m), 
				datetime_formatted = m.datetime_created.strftime("%b-%d-%Y, %H:%M:%S"), 
				datetime_layman = duration(dt_now, m.datetime_created.replace(tzinfo = None)),
				is_recent = (timedelta - (dt_now - m.datetime_created.replace(tzinfo = None))).days >= 0) 
			for m in markets]

		return JsonResponse({ "markets": markets_dict })

	except MarketModel.DoesNotExist:
		return JsonResponse({ "markets": [] })
		
def subscribe(request):	

	try:
		SubscriptionModel.objects.create(strategy = "A", email = request.GET["email"])
		return JsonResponse({ "success": True })
	except:
		return JsonResponse({ "success": False })

def unsubscribe(request):

	try:
		SubscriptionModel.objects.get(strategy = "A", email = request.GET["email"]).delete()
		return JsonResponse({ "success": True })
	except SubscriptionModel.DoesNotExist:
		return JsonResponse({ "success": False })

def email(request):

	try:
		receiver = SubscriptionModel.objects.filter(strategy = "A").values_list("email", flat = True)
		subject = "Strategy A: New Buy Signal"
		message = "Strategy A recent market: " + request.GET["market"]
		sender = settings.EMAIL_HOST_USER

		emails = tuple([tuple([subject, message, sender, [r]]) for r in receiver])
		send_mass_mail(emails)
	
	except SubscriptionModel.DoesNotExist:
		pass

	return JsonResponse({})