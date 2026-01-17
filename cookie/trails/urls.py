from django.urls import path

from .views import CalculatorView, CasesView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("calc/", CalculatorView.as_view(), name="calculator"),
    path("cases/", CasesView.as_view(), name="cases"),
]
