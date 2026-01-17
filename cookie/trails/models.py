from django.db import models

from .cookies import CookieVariety


class Family(models.Model):
    scout_name = models.CharField(max_length=100)
    email = models.EmailField()
    grade = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "families"

    def __str__(self):
        return f"{self.scout_name} (grade {self.grade}) <{self.email}>"


class EventType(models.TextChoices):
    # Family takes physical custody of troop cookies
    PICKUP = "pickup", "Pickup"

    # Family returns troop cookies to troop
    RETURN = "return", "Return"

    # Family reports cookie sales count
    COUNT = "count", "Count"


def _default_count_data() -> dict[str, int]:
    # This *has* to be a named function, not a lambda or just a dict literal,
    # because it is used as the default factory for a JSONField.
    return {variety.value: 0 for variety in CookieVariety}


class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    event_type = models.CharField(
        max_length=20, choices=EventType.choices, db_index=True
    )
    family = models.ForeignKey(Family, on_delete=models.PROTECT, related_name="events")
    updated_at = models.DateTimeField(auto_now=True)
    count_data = models.JSONField(default=_default_count_data)

    class Meta:
        ordering = ["created_at"]

    @property
    def counts(self) -> dict[CookieVariety, int]:
        return {
            CookieVariety(variety): count for variety, count in self.count_data.items()
        }

    @counts.setter
    def counts(self, value: dict[CookieVariety, int]) -> None:
        self.count_data = {variety.value: count for variety, count in value.items()}

    @property
    def total_count(self) -> int:
        return sum(self.counts.values())

    def count_for_variety(self, variety: CookieVariety) -> int:
        return self.count_data.get(variety.value, 0)

    def __str__(self):
        return f"{self.event_type} - {self.family}"
