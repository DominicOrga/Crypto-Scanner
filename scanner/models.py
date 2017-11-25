from django.db import models

# Create your models here.
class RsiModel(models.Model):
	market = models.CharField(max_length = 11, default = "")
	ave_gain = models.FloatField()
	ave_loss = models.FloatField()
	datetime = models.DateTimeField()

	def save(self, *args, **kwargs):
		objects = RsiModel.objects.all()

		if objects.count() >= 200:
			objects.first().delete()

		super(RsiModel, self).save(*args, **kwargs)

class MarketModel(models.Model):
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

	def save(self, *args, **kwargs):
		objects = MarketModel.objects.all()

		if objects.count() >= 200:
			objects.first().delete()

		super(MarketModel, self).save(*args, **kwargs)

class MarketGroupModel(models.Model):
	markets = models.ManyToManyField(MarketModel)

	def __str__(self):
		return " ".join(m.market[4:] for m in self.markets.all())

	def save(self, *args, **kwargs):
		objects = MarketGroupModel.objects.all()

		if objects.count() >= 5:
			objects.first().delete()

		super(MarketGroupModel, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):

		for m in self.markets.all():
			m.delete()
		
		super(MarketGroupModel, self).delete(*args, **kwargs)