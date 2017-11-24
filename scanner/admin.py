from django.contrib import admin
from .models import RsiModel, MarketModel, MarketGroupModel

class RsiModelAdmin(admin.ModelAdmin):
	list_display = ("market", "ave_gain", "ave_loss", "datetime")

class MarketModelAdmin(admin.ModelAdmin):
	list_display = ("market", "base_volume", "bid", "ask", "last", "previous_day", "change_24h", "change_12h", "change_6h", "rsi")

# Register your models here.
admin.site.register(RsiModel, RsiModelAdmin)
admin.site.register(MarketModel, MarketModelAdmin)
admin.site.register(MarketGroupModel)