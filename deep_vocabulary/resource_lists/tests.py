from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from test_plus.test import TestCase


class ResourceListViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            email="email@example.com",
            password="password"
        )

    def test_reading_lists_view(self):
        self.get("all_reading_lists")
        self.response_200()

    def test_user_reading_lists_view(self):
        self.client.force_login(self.user)
        self.get("user_reading_lists", user_pk=self.user.pk)
        self.response_200()

    def test_user_reading_lists_view_permission_denied(self):
        self.client.force_login(self.user)
        with self.assertRaises(PermissionDenied):
            self.get("user_reading_lists", user_pk=User.objects.last().pk + 1)
