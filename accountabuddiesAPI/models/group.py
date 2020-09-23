from django.db import models
from django.contrib.auth.models import User
from .account import Account

class Group(models.Model):

    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    # Limit of people in the group
    size = models.PositiveSmallIntegerField(default=5)
    # One member is the default, if he created the group he is on the group
    # Number of people currently in the group
    population = models.PositiveSmallIntegerField(default=1) 
    class Meta:
        verbose_name = ("Group")
        verbose_name_plural = ("Groups")


    def get_absolute_url(self):
        return reverse("Group_detail", kwargs={"pk": self.pk})