from django import forms

from .cookies import COOKIE_COLORS, CookieVariety
from .models import EventType, Family


class CookieCountForm(forms.Form):
    """Form for submitting cookie counts (used by families)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for variety in CookieVariety:
            self.fields[f"count_{variety.value}"] = forms.IntegerField(
                min_value=0,
                required=False,
                initial=0,
            )

    def get_count_data(self) -> dict[str, int]:
        """Extract cookie count data from cleaned form data."""
        return {
            variety.value: self.cleaned_data.get(f"count_{variety.value}") or 0
            for variety in CookieVariety
        }


class PickupReturnEventForm(CookieCountForm):
    """Form for admin to record pickup/return events."""

    family = forms.ModelChoiceField(queryset=Family.objects.all())
    event_type = forms.ChoiceField(
        choices=[
            (EventType.PICKUP, "Pickup (troop → family)"),
            (EventType.RETURN, "Return (family → troop)"),
        ]
    )


class FamilyLoginForm(forms.Form):
    """Form for family email-based login."""

    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        try:
            self.family = Family.objects.get(email__iexact=email)
        except Family.DoesNotExist:
            raise forms.ValidationError("Email not found. Please try again.")
        return email


class CookieCountWidget(forms.Widget):
    """Widget that displays separate number inputs for each cookie variety."""

    template_name = "trails/widgets/cookie_count_widget.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Parse value if it's a string (from form submission)
        if isinstance(value, str):
            import json

            try:
                value = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                value = {}

        # Build variety data with colors
        varieties = []
        for variety in CookieVariety:
            varieties.append(
                {
                    "key": variety.value,
                    "label": variety.label,
                    "color": COOKIE_COLORS[variety],
                    "value": value.get(variety.value, 0) if value else 0,
                }
            )
        context["varieties"] = varieties
        return context

    def value_from_datadict(self, data, files, name):
        import json

        result = {}
        for variety in CookieVariety:
            field_name = f"{name}_{variety.value}"
            try:
                result[variety.value] = int(data.get(field_name, 0))
            except (ValueError, TypeError):
                result[variety.value] = 0
        return json.dumps(result)
