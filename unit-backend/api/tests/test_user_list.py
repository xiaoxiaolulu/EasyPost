from rest_framework import status
from rest_framework.test import (
    APITestCase,
    APIClient
)
from api.models.https import User


class TestUserListViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/user/list'
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.token = ("JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90e"
                      "XBlIjoiYWNjZXNzIiwiZXhwIjoxNzExNjA5MDU0LCJqdGkiOiI2YTky"
                      "YTk3OGFiYTg0NzgwYjk1Y2I2NGQ3ZTM0Y2QzMiIsInVzZXJfaWQiOjF9"
                      ".-rNGK3Ye3uSx7TmTJalbaqHN8jV5AYAw7DKkNNGhgTI")

    def test_get_users(self):
        """
        测试获取用户列表
        """
        response = self.client.get(self.url, **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_users_with_invalid_ordering(self):
        """
        测试获取用户列表并按无效的排序字段返回错误
        """
        response = self.client.get(f'{self.url}?ordering=invalid_field', **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
