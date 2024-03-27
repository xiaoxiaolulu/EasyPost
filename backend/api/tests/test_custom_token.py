from rest_framework.test import (
    APITestCase,
    APIClient
)
from api.models.user import User
import random


class UserFactory:
    """
    创建测试用户的工厂类。
    """

    @staticmethod
    def create_user(**kwargs):
        """
        创建测试用户。

        :param kwargs: 关键字参数，用于传递给 `User` 模型的构造函数。
        :return: 创建的测试用户。
        :rtype: django.contrib.auth.models.User
        """
        return User.objects.create_user(**kwargs)


class TestCustomJsonWebToken(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/login/'
        self.user = UserFactory.create_user(username=random.randint(0, 999), password="123456")

    def test_post_valid_credentials(self):
        """
        测试使用有效凭据进行POST请求
        """
        response = self.client.post(
            self.url,
            data={
                'username': self.user.username,
                'password': '123456',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)

        self.assertIn('操作成功', str(response.data))

    def test_post_invalid_credentials(self):
        """
        测试使用无效凭据进行POST请求
        """
        response = self.client.post(
            self.url,
            data={
                'username': self.user.username,
                'password': 'wrong_password',
            },
            format='json',
        )
        self.assertIn('given credentials', str(response.data))

    def test_post_missing_fields(self):
        """
        测试使用缺少字段的POST请求
        """
        response = self.client.post(
            self.url,
            data={
                'username': self.user.username,
            },
            format='json',
        )
        self.assertIn('password', str(response.data))
