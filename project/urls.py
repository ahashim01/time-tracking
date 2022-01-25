from django.urls import path

from project import views

urlpatterns = [
    path("", views.ProjectListCreateAPIView.as_view(), name="projects"),
    path("<int:pk>/", views.ProjectRetrieveUpdateDestroyAPIView.as_view()),
    path("tasks/", views.TaskListCreateAPIView.as_view(), name="tasks"),
    path("tasks/<int:pk>/", views.TaskRetrieveUpdateDestroyAPIView.as_view()),
    path("tasks/<int:pk>/start/", views.EntryStartAPIView.as_view()),
    path("tasks/<int:pk>/end/", views.EntryEndAPIView.as_view()),
]
