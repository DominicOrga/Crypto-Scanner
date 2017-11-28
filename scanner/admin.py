from django.contrib import admin
from .models import RsiModel, MarketModel, MarketGroupModel

class RsiModelAdmin(admin.ModelAdmin):
	list_display = ("market", "ave_gain", "ave_loss", "datetime")

class MarketModelAdmin(admin.ModelAdmin):
	list_display = ("datetime_display", "market", "base_volume", "bid", "ask", "last", "previous_day", "change_24h", "change_12h", "change_6h", "rsi")

	def datetime_display(self, obj):
		return obj.datetime_created.strftime("%b-%d-%Y, %H:%M:%S")

class MarketGroupModelAdmin(admin.ModelAdmin):
	list_display = ("datetime_display", "markets_display")

	def datetime_display(self, obj):
		return obj.datetime_created.strftime("%b-%d-%Y, %H:%M:%S")

	def markets_display(self, obj):
		return obj

# Register your models here.
admin.site.register(RsiModel, RsiModelAdmin)
admin.site.register(MarketModel, MarketModelAdmin)
admin.site.register(MarketGroupModel, MarketGroupModelAdmin)