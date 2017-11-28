from django.conf.urls import url
from . import views
from . import services

urlpatterns = [
	url(r'^$', views.load_scanner, name="scanner"),
	url(r'^scan/', views.scan, name="scan"),
	url(r'^lastmarketupdate', views.last_market_update, name="last_market_update")
]

services.MarketUpdate().run()