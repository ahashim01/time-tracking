from django.shortcuts import get_object_or_404
from rest_framework import authentication, status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from project import models, serializers
from timetracking import permissions as custom_permissions

# Project APIs
class ProjectListCreateAPIView(generics.ListCreateAPIView):
    """
    API to list all the projects for the authenticated user and create
    new project for the authenticated user

    * Requires token authentication.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        """
        This view should return a list of all the projects
        for the currently authenticated user.
        """
        return models.Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        This will pre-define the authenticated user in serializer data
        """
        serializer.save(user=self.request.user)


class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API for retrive, update or destroy a certain project
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsAuthorized]
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class TaskListCreateAPIView(generics.ListCreateAPIView):
    """
    API to list all the tasks for the authenticated user and create
    new task for the authenticated user

    * Requires token authentication.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        """
        This view should return a list of all the projects
        for the currently authenticated user.
        """
        return models.Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        This will pre-define the authenticated user in serializer data
        """
        serializer.save(user=self.request.user)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API for retrive, update or destroy a certain project
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsAuthorized]
    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
