from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = ("Account")
        verbose_name_plural = ("Accounts")

    # def __str__(self):
    #     return f'{self.user.first_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse("Account_detail", kwargs={"pk": self.pk})
