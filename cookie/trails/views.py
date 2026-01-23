from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from .cookies import COOKIE_COLORS, COOKIE_POPULARITY, CookieVariety
from .family_auth import (
    clear_current_family,
    get_current_family,
    requires_family,
    set_current_family,
)
from .models import Event, EventType, Family


def _build_varieties_list(
    count_data: dict[str, int] | None = None, count_key: str = "count"
):
    """Build cookie varieties list in popularity order with colors.

    If count_data is provided, adds values under the specified count_key.
    """
    varieties = []
    for variety_code in COOKIE_POPULARITY.keys():
        cookie = CookieVariety(variety_code)
        color = COOKIE_COLORS.get(cookie, "#CCCCCC")
        hex_color = color.lstrip("#")
        r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        text_dark = luminance > 0.5
        variety = {
            "code": variety_code,
            "label": cookie.label,
            "color": color,
            "text_dark": text_dark,
        }
        if count_data is not None:
            variety[count_key] = count_data.get(variety_code, 0)
        varieties.append(variety)
    return varieties


def _parse_count_data(post_data) -> dict[str, int]:
    """Parse cookie count data from POST request."""
    count_data = {}
    for variety in CookieVariety:
        value = post_data.get(f"count_{variety.value}", "0")
        try:
            count_data[variety.value] = int(value) if value else 0
        except ValueError:
            count_data[variety.value] = 0
    return count_data


class HomeView(TemplateView):
    template_name = "home.html"


class CalculatorView(TemplateView):
    template_name = "calculator.html"


class CasesView(TemplateView):
    template_name = "cases.html"


@method_decorator(requires_family, name="dispatch")
class CountView(TemplateView):
    template_name = "count.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        family = get_current_family(self.request)

        # Get last count event for this family, if any
        last_count = (
            Event.objects.filter(family=family, event_type=EventType.COUNT)
            .order_by("-created_at")
            .first()
        )

        last_data = last_count.count_data if last_count else None
        context["varieties"] = _build_varieties_list(last_data, "last_value")
        context["has_previous"] = last_count is not None
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        family = get_current_family(request)
        if not family:
            return redirect("family_login")

        event = Event.objects.create(
            family=family,
            event_type=EventType.COUNT,
            count_data=_parse_count_data(request.POST),
        )

        return redirect("count_success", event_id=event.pk)


@method_decorator(requires_family, name="dispatch")
class CountSuccessView(TemplateView):
    template_name = "count_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        family = get_current_family(self.request)
        event_id = self.kwargs.get("event_id")

        # Get the event and verify it belongs to this family
        try:
            event = Event.objects.get(
                pk=event_id, family=family, event_type=EventType.COUNT
            )
        except Event.DoesNotExist:
            context["event"] = None
            return context

        varieties = _build_varieties_list(event.count_data)
        context["event"] = event
        context["varieties"] = varieties
        context["total"] = sum(v["count"] for v in varieties)
        return context


class FamilyLoginView(TemplateView):
    template_name = "family_login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "")
        context["error"] = self.request.GET.get("error", "")
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.POST.get("email", "").strip().lower()
        next_url = request.POST.get("next", "") or "/"

        try:
            family = Family.objects.get(email__iexact=email)
            set_current_family(request, family)
            return redirect(next_url)
        except Family.DoesNotExist:
            return redirect(f"{request.path}?next={next_url}&error=1")


class FamilyLogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        clear_current_family(request)
        return redirect("home")


@method_decorator(staff_member_required, name="dispatch")
class AdminEventView(TemplateView):
    template_name = "admin_event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["varieties"] = _build_varieties_list()
        context["families"] = Family.objects.all().order_by("scout_name")
        context["event_types"] = [
            {
                "value": EventType.PICKUP,
                "label": "Pickup (troop → family)",
                "description": "Family takes cookies from troop inventory",
            },
            {
                "value": EventType.RETURN,
                "label": "Return (family → troop)",
                "description": "Family returns cookies to troop inventory",
            },
        ]
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        family_id = request.POST.get("family")
        event_type = request.POST.get("event_type")

        # Validate family
        try:
            family = Family.objects.get(pk=family_id)
        except (Family.DoesNotExist, ValueError):
            return redirect("admin_event")

        # Validate event type
        if event_type not in (EventType.PICKUP, EventType.RETURN):
            return redirect("admin_event")

        event = Event.objects.create(
            family=family,
            event_type=event_type,
            count_data=_parse_count_data(request.POST),
        )

        return redirect("admin_event_success", event_id=event.pk)


@method_decorator(staff_member_required, name="dispatch")
class AdminEventSuccessView(TemplateView):
    template_name = "admin_event_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get("event_id")

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            context["event"] = None
            return context

        varieties = _build_varieties_list(event.count_data)
        context["event"] = event
        context["varieties"] = varieties
        context["total"] = sum(v["count"] for v in varieties)
        return context
