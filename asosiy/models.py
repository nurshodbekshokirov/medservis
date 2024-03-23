from django.db import models
from django.contrib.auth.models import User


class Mijoz(models.Model):
    ism = models.CharField(max_length=50)
    fam = models.CharField(max_length=50)
    jsshir = models.CharField(max_length=30)
    manzil = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return f"{self.ism, self.fam}"


class Emlama(models.Model):
    nom = models.TextField()
    sanasi = models.DateField()
    olindi = models.BooleanField()
    mijoz = models.ForeignKey(Mijoz, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.nom,  self.mijoz}"

# Create your models here.
