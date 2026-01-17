from typing import Any

from django.contrib import admin
from django.contrib.admin.decorators import display
from django.db import models
from django.http import HttpRequest

from cookie.admin import admin_site

from .cookies import COOKIE_COLORS, CookieVariety
from .forms import CookieCountWidget
from .models import Event, Family


class FamilyAdmin(admin.ModelAdmin):
    list_display = ("scout_name", "grade", "email")
    search_fields = ("scout_name", "email")
    search_help_text = "Search by scout name or parent email"

    def change_view(
        self,
        request: HttpRequest,
        object_id: str,
        form_url: str = "",
        extra_context: dict | None = None,
    ):
        extra_context = extra_context or {}
        extra_context["cookie_varieties"] = [
            {"value": v.value, "color": COOKIE_COLORS[v]} for v in CookieVariety
        ]
        return super().change_view(request, object_id, form_url, extra_context)


admin_site.register(Family, FamilyAdmin)


def make_variety_column(variety: CookieVariety) -> Any:
    @display(description=variety.value)
    def column(obj: Event) -> int:
        return obj.count_for_variety(variety)

    column.__name__ = f"count_{variety.value}"
    return column


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "created_at",
        "event_type",
        "family",
        *[make_variety_column(v) for v in CookieVariety],
        "total",
    ]
    ordering = ["created_at"]
    search_fields = ["family__scout_name", "family__email"]
    search_help_text = "Search by scout name or parent email"
    # list_filter = ["event_type"]

    formfield_overrides = {
        models.JSONField: {"widget": CookieCountWidget},
    }

    def changelist_view(self, request: HttpRequest, extra_context: dict | None = None):
        extra_context = extra_context or {}
        extra_context["cookie_colors"] = {
            v.value: COOKIE_COLORS[v] for v in CookieVariety
        }
        return super().changelist_view(request, extra_context)

    @display(description="total")
    def total(self, obj: Event) -> int:
        return obj.total_count


admin_site.register(Event, EventAdmin)
