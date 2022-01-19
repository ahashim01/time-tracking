from django.urls import path

from project import views

urlpatterns = [
    path("", views.ProjectListCreateAPIView.as_view(), name="projects"),
    path("<int:pk>/", views.ProjectRetrieveUpdateDestroyAPIView.as_view()),
]
