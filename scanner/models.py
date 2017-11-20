from django.db import models

# Create your models here.
class Rsi(models.Model):
	ave_gain = models.FloatField()
	ave_loss = models.FloatField()
	datetime = models.DateTimeField()