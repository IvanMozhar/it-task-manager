from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workers"
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name}) - {self.position}"

    def get_absolute_url(self):
        return reverse("manager:worker-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=263)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Task(models.Model):
    name = models.CharField(max_length=263, unique=True)
    description = models.TextField(max_length=600, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority_choices = (
        ("Low", "Low"),
        ("High", "High"),
        ("Urgent", "Urgent"),
    )
    priority = models.CharField(
        max_length=63,
        choices=priority_choices
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    tags = models.ManyToManyField(Tag, related_name="tasks")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}: {self.deadline} {self.is_completed}"
