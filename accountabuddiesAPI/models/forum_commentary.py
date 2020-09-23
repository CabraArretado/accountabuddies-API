from django.db import models
from django.contrib.auth.models import User
from .group import Group
from .forum_post import ForumPost

class ForumCommentary(models.Model):

    # In case the user is deleted the post still there
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
    null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("GroupUser_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = ("ForumCommentary")
        verbose_name_plural = ("ForumCommentaries")