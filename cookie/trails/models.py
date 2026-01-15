from decimal import Decimal

from django.db import models


class CookieVariety(models.TextChoices):
    ADVENTUREFULS = "Advf", "Adventurefuls"
    LEMON_UPS = "Lmup", "Lemon-Ups"
    TREFOILS = "Tre", "Trefoils"
    DO_SI_DOS = "D-S-D", "Do-si-dos"
    SAMOAS = "Sam", "Samoas"
    TAGALONGS = "Tags", "Tagalongs"
    THIN_MINTS = "TMint", "Thin Mints"
    EXPLOREMORES = "Exp", "Exploremores"
    TOFFEE_TASTICS = "Toff", "Toffee-tastics"


COOKIE_COSTS = {
    CookieVariety.ADVENTUREFULS: Decimal("6.00"),
    CookieVariety.LEMON_UPS: Decimal("6.00"),
    CookieVariety.TREFOILS: Decimal("6.00"),
    CookieVariety.DO_SI_DOS: Decimal("6.00"),
    CookieVariety.SAMOAS: Decimal("6.00"),
    CookieVariety.TAGALONGS: Decimal("6.00"),
    CookieVariety.THIN_MINTS: Decimal("6.00"),
    CookieVariety.EXPLOREMORES: Decimal("6.00"),
    CookieVariety.TOFFEE_TASTICS: Decimal("7.00"),
}


# These match eBudde's 2026 color scheme
COOKIE_COLORS = {
    CookieVariety.ADVENTUREFULS: "#D5CA9F",
    CookieVariety.LEMON_UPS: "#EDDF3E",
    CookieVariety.TREFOILS: "#005BAA",
    CookieVariety.DO_SI_DOS: "#FCC56A",
    CookieVariety.SAMOAS: "#7D4199",
    CookieVariety.TAGALONGS: "#E51A40",
    CookieVariety.THIN_MINTS: "#00A654",
    CookieVariety.EXPLOREMORES: "#EB9F94",
    CookieVariety.TOFFEE_TASTICS: "#00CABE",
}


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
