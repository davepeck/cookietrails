from django.db import models


class Family(models.Model):
    scout_name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "families"

    def __str__(self):
        return f"{self.scout_name} <{self.email}>"


class EventType(models.TextChoices):
    DISTRIBUTION = "distribution", "Distribution"
    RETURN = "return", "Return"
    COUNT = "count", "Count"


class Event(models.Model):
    family = models.ForeignKey(Family, on_delete=models.PROTECT, related_name="events")
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event_type} - {self.family}"
