from django.shortcuts import get_object_or_404
from rest_framework import authentication, status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from project import models, serializers
from timetracking import permissions as custom_permissions


class ListProjectsAPIView(APIView):
    """
    API to list all the projects for the authenticated user

    * Requires token authentication.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return All the user's projects
        """
        user = request.user
        projects = models.Project.objects.filter(user=user)

        # validate if the the user have projects or not
        if not projects:
            return Response(
                {"You don't have projects, please add new project"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = serializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectAPIView(APIView):
    """
    API for create a new project for the authenticated user

    * Requires token authentication.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Create a new user's project
        """
        # Pre-define the authenticated user in request data
        request.data["user"] = request.user.id
        serializer = serializers.ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API for retrive, update or destroy a certain project
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsAuthorized]
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()
