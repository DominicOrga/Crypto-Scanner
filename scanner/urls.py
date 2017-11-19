from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.scan),
	url(r'^rescan/', views.rescan, name="rescan")
]