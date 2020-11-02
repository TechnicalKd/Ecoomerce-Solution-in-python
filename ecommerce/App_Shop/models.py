from django.db import models

# Create your models here.
class Category(models.Model):
	title = models.CharField(max_length=100)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "categories"

	def __str__(self):
		return self.title




class Product(models.Model):
	main_image = models.ImageField(upload_to="product")
	name = models.CharField(max_length=264)
	category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category")
	preview_text = models.TextField(verbose_name="Preview Text")
	details_text = models.TextField(verbose_name="Description")
	price = models.FloatField()
	old_price = models.FloatField()
	default_value = models.FloatField(default="0.00")
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-created']



