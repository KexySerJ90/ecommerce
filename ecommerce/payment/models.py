from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class ShippingAdress(models.Model):
    full_name = models.CharField(max_length=300)
    email=models.EmailField(max_length=255)
    address1=models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    city=models.CharField(max_length=255)
    state=models.CharField(max_length=255,null=True, blank=True)
    zipcode=models.CharField(max_length=255,null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural="Shipping Adress"

    def __str__(self):
        return 'Shipping Adress - ' + str(self.id)
