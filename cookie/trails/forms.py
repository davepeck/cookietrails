from django import forms

from .cookies import COOKIE_COLORS, CookieVariety


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
