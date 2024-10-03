from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse

# Create your models here.

class ReimburseModel(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	source = models.FileField(upload_to='uploads', null=True, blank=True, validators=[FileExtensionValidator(['csv'])])
	destination = models.FileField(upload_to='uploads', null=True, blank=True)

	def get_absolute_url(self):
		return reverse('converter:reimburse')
	
class MileageModel(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	source = models.FileField(upload_to='uploads', null=True, blank=True, validators=[FileExtensionValidator(['csv'])])
	destination = models.FileField(upload_to='uploads', null=True, blank=True)

	def get_absolute_url(self):
		return reverse('converter:mileage')