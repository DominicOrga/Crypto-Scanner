from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.load_strata, name = "strata"),
	url(r'^processed_data$', views.processed_data, name="processed_data")
]