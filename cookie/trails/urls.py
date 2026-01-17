from django.urls import path

from .views import (
    CalculatorView,
    CasesView,
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
    path("family/login/", FamilyLoginView.as_view(), name="family_login"),
    path("family/logout/", FamilyLogoutView.as_view(), name="family_logout"),
]
