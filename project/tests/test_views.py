from django.contrib.auth.models import User
from django.urls import reverse
from project import factories, models
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class ProjectTest(APITestCase):
    def setUp(self):
        """
        We want to create projects batch for different users
        """
        self.test_user1 = User.objects.create_user(
            "testuser1", "test1@example.com", "test1password"
        )
        self.user1_token = Token.objects.get(user=self.test_user1).key

        self.test_user2 = User.objects.create_user(
            "testuser2", "test2@example.com", "test2password"
        )
        self.user2_token = Token.objects.get(user=self.test_user2).key

        factories.ProjectFactory.create_batch(5, user=self.test_user1)
        factories.ProjectFactory.create_batch(5, user=self.test_user2)

        # URLs
        self.projects_url = reverse("projects")

    def test_get_projects_ownership(self):
        """
        Ensure that the projects return are owned by the authenticated user
        """
        response = self.client.get(
            self.projects_url, HTTP_AUTHORIZATION=f"Token {self.user1_token}"
        )
        self.assertEqual(models.Project.objects.count(), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            models.Project.objects.filter(user=self.test_user1).count(),
        )
        for project in response.data:
            self.assertEqual(project["user"], self.test_user1.id)

    def test_project_create(self):
        """
        Ensure that the created project's owner is the user authenticated
        """
        data = {"title": "Test Project"}
        response = self.client.post(
            self.projects_url, data=data, HTTP_AUTHORIZATION=f"Token {self.user1_token}"
        )
        self.assertEqual(response.data["user"], self.test_user1.id)

    def test_project_update(self):
        """
        Ensure that the authenticated user can only update owned projects
        """
        # Get another user's project and test the authority of it to update
        user2_project = self.test_user2.projects.latest("id")
        data = {"title": "Title updated"}
        response = self.client.put(
            f"{self.projects_url}{user2_project.id}/",
            data=data,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check project update
        user1_project = self.test_user1.projects.latest("id")
        data = {"title": "Title updated"}
        response = self.client.put(
            f"{self.projects_url}{user1_project.id}/",
            data=data,
            HTTP_AUTHORIZATION=f"Token {self.user1_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
