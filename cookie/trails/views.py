from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from .family_auth import (
    clear_current_family,
    requires_family,
    set_current_family,
)
from .models import Family


class HomeView(TemplateView):
    template_name = "home.html"


class CalculatorView(TemplateView):
    template_name = "calculator.html"


class CasesView(TemplateView):
    template_name = "cases.html"


@method_decorator(requires_family, name="dispatch")
class CountView(TemplateView):
    template_name = "count.html"


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
