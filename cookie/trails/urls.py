from django.urls import path

from .views import (
    CalculatorView,
    CasesView,
    CountSuccessView,
    CountView,
    FamilyLoginView,
    FamilyLogoutView,
    HomeView,
    InitialOrdersCsvView,
    InitialOrderSuccessView,
    InitialOrderView,
    PickupReturnEventSuccessView,
    PickupReturnEventView,
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
    path("events/initial-order/", InitialOrderView.as_view(), name="initial_order"),
    path(
        "events/initial-order/<int:event_id>/success/",
        InitialOrderSuccessView.as_view(),
        name="initial_order_success",
    ),
    path("family/login/", FamilyLoginView.as_view(), name="family_login"),
    path("family/logout/", FamilyLogoutView.as_view(), name="family_logout"),
    # Admin-only views (staff_member_required)
    path("staff/event/", PickupReturnEventView.as_view(), name="pickup_return_event"),
    path(
        "staff/event/<int:event_id>/success/",
        PickupReturnEventSuccessView.as_view(),
        name="pickup_return_event_success",
    ),
    path(
        "staff/initial-orders.csv",
        InitialOrdersCsvView.as_view(),
        name="initial_orders_csv",
    ),
]
