from rest_framework import status
from rest_framework.test import (
    APITestCase,
    APIClient
)
from api.models.project import Project


class ProjectDestroyViewSetTests(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.client = APIClient()
        self.url = f'/api/project/delete/{self.project.pk}'
        self.token = ("JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
                      "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNz"
                      "ExNjc4MjQ0LCJqdGkiOiIwZTZiZTFjODc3YzE0YmRh"
                      "YjQ5MTNmYjRhNGVkYTIzMiIsInVzZXJfaWQiOjF9.R"
                      "ICMkSeaSsSheMS7foduBEMUOLKcTlpctWxv_bQH7yE")

    def test_destroy_project_authenticated_user(self):
        response = self.client.delete(self.url, **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
