from django.db import models
from django.conf import settings

# Create your models here.

class BillingsAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	address = models.CharField(max_length=255, blank=True)
	zipcode = models.CharField(max_length=255, blank=True)
	city = models.CharField(max_length=255, blank=True)
	country = models.CharField(max_length=255, blank=True)


	def __str__(self):
		return f'{self.user.profile.username} Billing sAddress'

	def is_fully_filled(self):
			field_names = [f.name for f in self._meta.get_fields()]

			for field_name in field_names:
				value = getattr(self,field_name)
				if value is  None or value == '':
					return False
			return True
