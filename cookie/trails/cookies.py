from decimal import ROUND_HALF_UP, Decimal, localcontext

from django.db import models


class CookieVariety(models.TextChoices):
    ADVENTUREFULS = "Advf", "Adventurefuls"
    LEMON_UPS = "Lmup", "Lemon-ups"
    TREFOILS = "Tre", "Trefoils"
    DO_SI_DOS = "D-S-D", "Do-si-dos"
    SAMOAS = "Sam", "Samoas"
    TAGALONGS = "Tags", "Tagalongs"
    THIN_MINTS = "TMint", "Thin Mints"
    EXPLOREMORES = "Exp", "Exploremores"
    TOFFEE_TASTICS = "Toff", "Toffee-tastics"


COOKIE_COSTS: dict[CookieVariety, Decimal] = {
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
COOKIE_COLORS: dict[CookieVariety, str] = {
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


# Current as of Friday January 16, 2026
COOKIE_POPULARITY: dict[CookieVariety, float] = {
    CookieVariety.THIN_MINTS: 0.278,
    CookieVariety.SAMOAS: 0.208,
    CookieVariety.TAGALONGS: 0.142,
    CookieVariety.EXPLOREMORES: 0.099,
    CookieVariety.ADVENTUREFULS: 0.069,
    CookieVariety.TREFOILS: 0.065,
    CookieVariety.LEMON_UPS: 0.061,
    CookieVariety.DO_SI_DOS: 0.047,
    CookieVariety.TOFFEE_TASTICS: 0.031,
}


assert sum(COOKIE_POPULARITY.values()) == 1.0, (
    "Cookie popularity values must sum to 1.0"
)


def calculate_cookie_cost(varities: dict[CookieVariety, int]) -> Decimal:
    """Calculate the total cost for the given cookie varieties and their counts."""
    with localcontext() as ctx:
        ctx.prec = 28
        ctx.rounding = ROUND_HALF_UP

        total = Decimal("0.00")
        for variety, count in varities.items():
            cost_per_box = COOKIE_COSTS.get(variety, Decimal("0.00"))
            total += cost_per_box * count
        return total.quantize(Decimal("0.01"))


def calculate_distribution(total_boxes: int) -> dict[CookieVariety, int]:
    """Use cookie popularity to estimate a distribution of cookie varieties."""
    distribution: dict[CookieVariety, int] = {}
    for variety, popularity in COOKIE_POPULARITY.items():
        estimated_count = int(round(total_boxes * popularity))
        distribution[variety] = estimated_count

    # Adjust for rounding errors by distributing across varieties by popularity
    diff = total_boxes - sum(distribution.values())
    assert abs(diff) <= total_boxes, (
        f"Difference should be less than total boxes: {diff}"
    )
    varieties_by_popularity = list(COOKIE_POPULARITY.keys())
    idx = 0
    while diff != 0:
        variety = varieties_by_popularity[idx % len(varieties_by_popularity)]
        if diff > 0:
            distribution[variety] += 1
            diff -= 1
        else:
            if distribution[variety] > 0:
                distribution[variety] -= 1
                diff += 1
        idx += 1

    return distribution


BOXES_PER_CASE = 12
CASE_THRESHOLD = 5


def calculate_cases(
    boxes: dict[CookieVariety, int], *, threshold: int = CASE_THRESHOLD
) -> dict[CookieVariety, int]:
    """Calculate the number of cases suggested for each cookie variety."""
    cases: dict[CookieVariety, int] = {}
    # CONSIDER: if the box count modulo 12 is beneath the threshold, do we
    # want to round down instead of up? For now, we always round up if
    # above the threshold aka 13 boxes => 2 cases, 17 boxes => 2 cases.
    for variety, box_count in boxes.items():
        if box_count >= threshold:
            num_cases = (box_count + BOXES_PER_CASE - 1) // BOXES_PER_CASE
            cases[variety] = num_cases
        else:
            cases[variety] = 0
    return cases
