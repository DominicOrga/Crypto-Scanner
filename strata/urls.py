from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.load_strata, name = "strata"),
	url(r'^stratamarkets$', views.strata_markets, name="strata_markets")
]