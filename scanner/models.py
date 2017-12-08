from django.db import models
from django.utils import timezone

class RsiModel(models.Model):
	market = models.CharField(max_length = 11, default = "")
	ave_gain = models.FloatField()
	ave_loss = models.FloatField()
	datetime = models.DateTimeField() # of last candle

	def save(self, *args, **kwargs):
		super(RsiModel, self).save(*args, **kwargs)

		objects = RsiModel.objects.all()
		excess = objects.count() - 200

		for i in range(excess):
			objects.first().delete()

class MarketModel(models.Model):
	datetime_created = models.DateTimeField(default = timezone.now)
	market = models.CharField(max_length = 11, default = "")
	base_volume = models.FloatField()
	bid = models.FloatField()
	ask = models.FloatField()
	last = models.FloatField()
	previous_day = models.FloatField()
	change_24h = models.FloatField()
	change_12h = models.FloatField()
	change_6h = models.FloatField()
	rsi  = models.FloatField()

	def __str__(self):
		return self.market

class MarketGroupModel(models.Model):
	datetime_created = models.DateTimeField(default = timezone.now)
	creation_delay_ms = models.FloatField(default = 0) # Time it takes for this MarketGroupModel to be created
	markets = models.ManyToManyField(MarketModel)

	def __str__(self):
		return " ".join(m.market[4:] for m in self.markets.all())

	def delete(self, *args, **kwargs):

		for m in self.markets.all():
			m.delete()
		
		super(MarketGroupModel, self).delete(*args, **kwargs)

class SubscriptionModel(models.Model):
	strategy = models.CharField(max_length = 2, default = "")
	email = models.EmailField()