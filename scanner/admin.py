from django.contrib import admin
from .models import RsiModel

class RsiModelAdmin(admin.ModelAdmin):
	list_display = ("market", "ave_gain", "ave_loss", "datetime")

# Register your models here.
admin.site.register(RsiModel, RsiModelAdmin)