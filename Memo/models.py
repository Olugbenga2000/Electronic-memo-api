from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Memo(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender_dept', blank=False, null=False)
    receivers = models.ManyToManyField(
        Department, related_name='memos',)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Staff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='users')
    department = models.OneToOneField(
        Department, on_delete=models.CASCADE, related_name='departments')
    # admin = models.OneToOneField(
    #     User, on_delete=models.CASCADE, related_name='admins')

    # class Meta:
    #     unique_together = ('user', 'department')

    def __str__(self):
        return self.user.username


class StarMemo(models.Model):
    memo = models.ForeignKey(
        Memo, on_delete=models.CASCADE, related_name='star_memos')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='myuser')
    isStarred = models.BooleanField(default=False)


class ReadMemo(models.Model):
    memo = models.ForeignKey(
        Memo, on_delete=models.CASCADE, related_name='read_memos')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='my_user')
    isRead = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
