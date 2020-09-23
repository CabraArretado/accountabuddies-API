from django.db import models
from django.contrib.auth.models import User
from .group import Group

class ForumPost(models.Model):

    # In case the user is deleted the post still there
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,
    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)

    def get_absolute_url(self):
        return reverse("ForumPost_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = ("ForumPost")
        verbose_name_plural = ("ForumPosts")