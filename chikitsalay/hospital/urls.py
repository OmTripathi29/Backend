from django.urls import path
from .views import hospital_search

urlpatterns = [
    path("search/", hospital_search, name="hospital-search"),
]