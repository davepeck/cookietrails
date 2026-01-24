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
from .forms import CookieCountForm, FamilyLoginForm, PickupReturnEventForm
from .models import CountUnit, Event, EventType, Family


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


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        family = get_current_family(self.request)
        if family:
            context["has_initial_order"] = Event.objects.filter(
                family=family, event_type=EventType.COOKIE_ORDER
            ).exists()
        return context


class CalculatorView(TemplateView):
    template_name = "calculator.html"


class CasesView(TemplateView):
    template_name = "cases.html"


class OrderHelperView(TemplateView):
    template_name = "order_helper.html"


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

        form = CookieCountForm(request.POST)
        if form.is_valid():
            event = Event.objects.create(
                family=family,
                event_type=EventType.COUNT,
                count_data=form.get_count_data(),
            )
            return redirect("count_success", event_id=event.pk)

        # Re-render with errors (though unlikely with optional int fields)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


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


@method_decorator(requires_family, name="dispatch")
class InitialOrderView(TemplateView):
    template_name = "initial_order.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        family = get_current_family(request)
        if family:
            # If family already has an order, redirect to success page
            existing_order = (
                Event.objects.filter(family=family, event_type=EventType.COOKIE_ORDER)
                .order_by("-created_at")
                .first()
            )
            if existing_order:
                return redirect("initial_order_success", event_id=existing_order.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["varieties"] = _build_varieties_list()
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        import json

        family = get_current_family(request)
        if not family:
            return redirect("family_login")

        form = CookieCountForm(request.POST)
        if form.is_valid():
            # Parse box breakdown from helper if provided
            extra_data: dict = {}
            box_breakdown_json = request.POST.get("box_breakdown")
            if box_breakdown_json:
                try:
                    extra_data["box_breakdown"] = json.loads(box_breakdown_json)
                except json.JSONDecodeError:
                    pass  # Ignore malformed JSON

            event = Event.objects.create(
                family=family,
                event_type=EventType.COOKIE_ORDER,
                unit=CountUnit.CASE,
                count_data=form.get_count_data(),
                extra=extra_data,
            )
            from django.urls import reverse

            return redirect(
                reverse("initial_order_success", kwargs={"event_id": event.pk})
                + "?new=1"
            )

        # Re-render with errors
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


@method_decorator(requires_family, name="dispatch")
class InitialOrderSuccessView(TemplateView):
    template_name = "initial_order_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        family = get_current_family(self.request)
        event_id = self.kwargs.get("event_id")

        # Check if this is a new submission or viewing a previous one
        context["is_new_submission"] = self.request.GET.get("new") == "1"

        # Get the event and verify it belongs to this family
        try:
            event = Event.objects.get(
                pk=event_id, family=family, event_type=EventType.COOKIE_ORDER
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
        context["form"] = kwargs.get("form", FamilyLoginForm())
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        form = FamilyLoginForm(request.POST)
        next_url = request.POST.get("next", "") or "/"

        if form.is_valid():
            set_current_family(request, form.family)
            return redirect(next_url)

        return self.render_to_response(self.get_context_data(form=form))


class FamilyLogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        clear_current_family(request)
        return redirect("home")


@method_decorator(staff_member_required, name="dispatch")
class PickupReturnEventView(TemplateView):
    template_name = "pickup_return_event.html"

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
        form = PickupReturnEventForm(request.POST)
        if form.is_valid():
            event = Event.objects.create(
                family=form.cleaned_data["family"],
                event_type=form.cleaned_data["event_type"],
                count_data=form.get_count_data(),
            )
            return redirect("pickup_return_event_success", event_id=event.pk)

        # Re-render with errors
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


@method_decorator(staff_member_required, name="dispatch")
class PickupReturnEventSuccessView(TemplateView):
    template_name = "pickup_return_event_success.html"

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


@method_decorator(staff_member_required, name="dispatch")
class InitialOrdersCsvView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        import csv

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="initial_orders.csv"'

        writer = csv.writer(response)

        # Header row
        variety_codes = list(COOKIE_POPULARITY.keys())
        header = ["Scout Name", "Email", "Grade", "Order Date"]
        header.extend(v.value for v in variety_codes)
        header.append("Total Cases")
        writer.writerow(header)

        # Build a map of family_id -> order for quick lookup
        orders = Event.objects.filter(event_type=EventType.COOKIE_ORDER)
        orders_by_family = {order.family.pk: order for order in orders}

        # Data rows - one per family, ordered by scout_name
        for family in Family.objects.order_by("scout_name"):
            order = orders_by_family.get(family.pk)
            row = [
                family.scout_name,
                family.email,
                family.grade,
                order.created_at.strftime("%Y-%m-%d %H:%M") if order else "",
            ]
            total = 0
            for variety in variety_codes:
                count = order.count_data.get(variety.value, 0) if order else 0
                row.append(count)
                total += count
            row.append(total)
            writer.writerow(row)

        return response
