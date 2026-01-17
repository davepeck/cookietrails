from functools import wraps
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from .models import Family

FAMILY_SESSION_KEY = "family_id"


def get_current_family(request: HttpRequest) -> Family | None:
    """Get the currently logged-in family from the session, if any."""
    family_id = request.session.get(FAMILY_SESSION_KEY)
    if family_id is None:
        return None
    try:
        return Family.objects.get(pk=family_id)
    except Family.DoesNotExist:
        # Family was deleted; clear stale session
        del request.session[FAMILY_SESSION_KEY]
        return None


def set_current_family(request: HttpRequest, family: Family) -> None:
    """Set the current family in the session."""
    request.session[FAMILY_SESSION_KEY] = family.pk


def clear_current_family(request: HttpRequest) -> None:
    """Clear the current family from the session."""
    request.session.pop(FAMILY_SESSION_KEY, None)


def requires_family(view_func: Any) -> Any:
    """
    Decorator for views that require a family to be logged in.
    Redirects to the family login page if no family is in session.
    """

    @wraps(view_func)
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if get_current_family(request) is None:
            login_url = reverse("family_login")
            next_url = request.get_full_path()
            return redirect(f"{login_url}?next={next_url}")
        return view_func(request, *args, **kwargs)

    return wrapper
