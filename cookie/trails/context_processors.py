from django.http import HttpRequest

from .family_auth import get_current_family


def family(request: HttpRequest) -> dict:
    """Add the current family to the template context."""
    return {"current_family": get_current_family(request)}
