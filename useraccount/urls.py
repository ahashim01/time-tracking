from django.urls import path

from . import views
from project import views as project_views

urlpatterns = [
    path("register/", views.UserCreate.as_view(), name="account-create"),
]
