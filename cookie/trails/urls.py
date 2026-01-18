from django.urls import path

from .views import (
    AdminEventSuccessView,
    AdminEventView,
    CalculatorView,
    CasesView,
    CountSuccessView,
    CountView,
    FamilyLoginView,
    FamilyLogoutView,
    HomeView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("calc/", CalculatorView.as_view(), name="calculator"),
    path("cases/", CasesView.as_view(), name="cases"),
    path("events/count/", CountView.as_view(), name="count"),
    path(
        "events/count/<int:event_id>/success/",
        CountSuccessView.as_view(),
        name="count_success",
    ),
    path("family/login/", FamilyLoginView.as_view(), name="family_login"),
    path("family/logout/", FamilyLogoutView.as_view(), name="family_logout"),
    # Admin-only views (staff_member_required)
    path("staff/event/", AdminEventView.as_view(), name="admin_event"),
    path(
        "staff/event/<int:event_id>/success/",
        AdminEventSuccessView.as_view(),
        name="admin_event_success",
    ),
]
