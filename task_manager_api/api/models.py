from django.db import models
from django.contrib.auth.models import User
from .utils import TASK_STATUS_CHOICES


class Dashboard(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User)


class Sprint(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField()
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, blank=True)
    status = models.CharField(
        max_length=2, choices=TASK_STATUS_CHOICES, default='TODO')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="tasks")
    assigned_to = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='assigned_tasks', default=None, null=True)
    sprint = models.ForeignKey(
        Sprint, on_delete=models.CASCADE, null=True)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)

    def __str__(self):
        for key, value in TASK_STATUS_CHOICES:
            if key == self.status:
                status = value

        return f'{self.title} - {status}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField(max_length=2000)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.content}'
