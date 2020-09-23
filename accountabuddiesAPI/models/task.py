from django.db import models
from .group import Group
from django.contrib.auth.models import User

class Task(models.Model):

    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100)
    due = models.DateTimeField()
    done = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Task")
        verbose_name_plural = ("Tasks")


    def get_absolute_url(self):
        return reverse("Task_detail", kwargs={"pk": self.pk})