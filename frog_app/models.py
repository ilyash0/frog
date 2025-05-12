from django.db import models
from datetime import date

from user.models import User


class FrogRarity(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)

    class Meta:
        db_table = "frog_app_frog_rarity"


class Frog(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rarity = models.ForeignKey(FrogRarity, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/frog_images/', null=True)
    users = models.ManyToManyField(User, through='FrogUser')


class FrogUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    frog = models.ForeignKey(Frog, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = "frog_app_frog_user"
        unique_together = ('user', 'frog')


class FrogAcquisition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    frog = models.ForeignKey(Frog, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        db_table = "frog_app_frog_acquisition"
        unique_together = ('user', 'date')

