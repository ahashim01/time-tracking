from datetime import datetime, timezone

from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from timetracking import permissions as custom_permissions

from project import models, serializers


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


class EntryStartAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsAuthorized]
    serializer_class = serializers.EntrySerializer

    def post(self, request, pk):
        """
        API to start track a task.
        """
        user = request.user
        task = user.tasks.get(id=pk)

        # check if there is any tracked task
        if user.entries.filter(is_tracked=True):
            return Response(
                {"message": "You already have a tracked task in progress."},
                status=status.HTTP_200_OK,
            )
        entry = models.Entry.objects.create(
            project=task.project,
            task=task,
            is_tracked=True,
            created_by=user,
            created_at=datetime.now(),
        )
        serializer = self.serializer_class(entry)
        return Response(
            {"status": "Start Tracking", "task": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class EntryEndAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsAuthorized]
    serializer_class = serializers.EntrySerializer

    def post(self, request, pk):
        """
        API to end tracking a task
        """
        user = request.user
        task = user.tasks.get(id=pk)
        try:
            entry = models.Entry.objects.get(
                project=task.project,
                task=task,
                is_tracked=True,
                created_by=request.user,
            )
        except models.Entry.DoesNotExist:
            return Response(
                {"message": "There is no tracked task with the provided data"},
                status=status.HTTP_404_NOT_FOUND,
            )

        tracked_minutes = int(
            (datetime.now(timezone.utc) - entry.created_at).total_seconds() / 60
        )

        if tracked_minutes < 1:
            tracked_minutes = 1

        entry.minutes = tracked_minutes
        entry.is_tracked = False
        entry.save()
        serializer = self.serializer_class(entry)
        return Response(
            {"status": "Stop Tracking", "task": serializer.data},
            status=status.HTTP_200_OK,
        )
