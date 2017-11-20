from django.db import models

# Create your models here.
class RsiModel(models.Model):
	market = models.CharField(max_length=11, default="")
	ave_gain = models.FloatField()
	ave_loss = models.FloatField()
	datetime = models.DateTimeField()

	def save(self, *args, **kwargs):
		objects = RsiModel.objects.all()

		if objects.count() >= 200:
			objects[0].delete()

		super(RsiModel, self).save(*args, **kwargs)

