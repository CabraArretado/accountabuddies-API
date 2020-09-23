from django.db import models
from django.contrib.auth.models import User
from .group import Group

class GroupUser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_adm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("GroupUser_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = ("GroupUser")
        verbose_name_plural = ("GroupUsers")