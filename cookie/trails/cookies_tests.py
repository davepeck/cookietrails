from decimal import Decimal

from .cookies import (
    COOKIE_COSTS,
    COOKIE_POPULARITY,
    CookieVariety,
    calculate_cases,
    calculate_cookie_cost,
    calculate_distribution,
)


def test_calculate_cookie_cost():
    varities = {
        CookieVariety.THIN_MINTS: 3,
        CookieVariety.SAMOAS: 2,
        CookieVariety.TOFFEE_TASTICS: 1,
    }
    total_cost = calculate_cookie_cost(varities)
    expected_cost = (
        COOKIE_COSTS[CookieVariety.THIN_MINTS] * 3
        + COOKIE_COSTS[CookieVariety.SAMOAS] * 2
        + COOKIE_COSTS[CookieVariety.TOFFEE_TASTICS] * 1
    )
    assert total_cost == expected_cost


def test_calculate_cookie_cost_empty():
    varities = {}
    total_cost = calculate_cookie_cost(varities)
    assert total_cost == Decimal("0.00")


def test_calculate_distribution():
    for total_boxes in range(0, 1001):
        distribution = calculate_distribution(total_boxes)

        # Check that the total boxes in the distribution matches the input
        assert sum(distribution.values()) == total_boxes

        # Check that more popular cookies have at least as many boxes as less popular ones
        sorted_varieties = sorted(
            CookieVariety,
            key=lambda v: COOKIE_POPULARITY[v],
            reverse=True,
        )
        for i in range(len(sorted_varieties) - 1):
            more_popular = sorted_varieties[i]
            less_popular = sorted_varieties[i + 1]
            assert distribution[more_popular] >= distribution[less_popular], (
                f"{more_popular} should have at least as many boxes as {less_popular}"
            )


def test_calculate_cases():
    boxes = {
        CookieVariety.THIN_MINTS: 57,
        CookieVariety.SAMOAS: 26,
        CookieVariety.LEMON_UPS: 7,
        CookieVariety.TOFFEE_TASTICS: 3,
    }
    cases = calculate_cases(boxes, threshold=5)

    assert cases[CookieVariety.THIN_MINTS] == 5
    assert cases[CookieVariety.SAMOAS] == 3
    assert cases[CookieVariety.LEMON_UPS] == 1
    assert cases[CookieVariety.TOFFEE_TASTICS] == 0
