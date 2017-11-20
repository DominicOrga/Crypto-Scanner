from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.load_scanner),
	url(r'^rescan/', views.scan, name="scan")
]