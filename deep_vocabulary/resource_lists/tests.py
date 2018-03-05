from django.db import IntegrityError

from test_plus.test import TestCase as TestCasePlus

from deep_vocabulary import factories

from . import models


class ResourceListModelTests(TestCasePlus):
    def setUp(self):
        self.user = factories.UserFactory.create()

    def test_resource_list_clone(self):
        reading_list = factories.ReadingListFactory.create()
        reading_list.duplicate(owner=self.user)

        self.assertEqual(models.ReadingList.objects.count(), 2)
        original, clone = models.ReadingList.objects.all()

        self.assertEqual(clone.owner_id, self.user.pk)
        self.assertEqual(clone.cloned_from_id, original.pk)
        self.assertEqual(clone.title, original.title)

        altered_fields = ["secret_key", "updated", "created"]
        for field in altered_fields:
            with self.subTest(field=field):
                self.assertNotEqual(
                    getattr(original, field),
                    getattr(clone, field)
                )

    def test_subscription_save_constraint(self):
        def add_subscription():
            models.ReadingListSubscription.objects.create(
                resource_list=reading_list,
                subscriber=self.user
            )
        reading_list = factories.ReadingListFactory.create()
        add_subscription()
        self.assertEqual(reading_list.subscriptions.count(), 1)
        with self.assertRaises(IntegrityError):
            add_subscription()


class ResourceListViewsTests(TestCasePlus):
    def setUp(self):
        self.user = factories.UserFactory.create()
        self.client.force_login(self.user)

    def test_list_views(self):
        views = ["reading_lists", "vocabulary_lists"]
        for view in views:
            with self.subTest(view=view):
                self.get(view)
                self.response_200()

    def test_user_list_views(self):
        views = ["user_reading_lists", "user_vocabulary_lists"]
        for view in views:
            with self.subTest(view=view):
                self.get(view, user_pk=self.user.pk)
                self.response_200()

    def test_user_list_views_permission_denied(self):
        views = ["user_reading_lists", "user_vocabulary_lists"]
        for view in views:
            with self.subTest(view=view):
                self.get(view, user_pk=self.user.pk + 1)
                self.response_403()

    def test_user_subscriptions_views(self):
        views = ["reading_list_subscriptions", "vocabulary_list_subscriptions"]
        for view in views:
            with self.subTest(view=view):
                self.get(view, user_pk=self.user.pk)
                self.response_200()

    def test_user_subscriptions_views_permission_denied(self):
        views = ["reading_list_subscriptions", "vocabulary_list_subscriptions"]
        for view in views:
            with self.subTest(view=view):
                self.get(view, user_pk=self.user.pk + 1)
                self.response_403()

    def test_list_detail_views(self):
        reading_list = factories.ReadingListFactory.create()
        vocabulary_list = factories.VocabularyListFactory.create()
        views = [
            ("reading_list", reading_list),
            ("vocabulary_list", vocabulary_list)
        ]
        for view, resource_list in views:
            with self.subTest(view=view):
                self.get(view, secret_key=resource_list.secret_key)
                self.response_200()

    def test_list_clone_views(self):
        reading_list = factories.ReadingListFactory.create()
        vocabulary_list = factories.VocabularyListFactory.create()
        views = [
            ("reading_list_clone", reading_list),
            ("vocabulary_list_clone", vocabulary_list)
        ]
        for view, resource_list in views:
            with self.subTest(view=view):
                self.assertEqual(resource_list._meta.model.objects.count(), 1)
                self.post(view, secret_key=resource_list.secret_key)
                self.response_302()
                self.assertEqual(resource_list._meta.model.objects.count(), 2)

    def test_list_subscribe_views(self):
        reading_list = factories.ReadingListFactory.create()
        vocabulary_list = factories.VocabularyListFactory.create()
        views = [
            ("reading_list_subscribe", reading_list),
            ("vocabulary_list_subscribe", vocabulary_list)
        ]
        for view, resource_list in views:
            with self.subTest(view=view):
                self.assertEqual(resource_list.subscriptions.count(), 0)
                self.post(view, secret_key=resource_list.secret_key)
                self.response_302()
                self.assertEqual(resource_list.subscriptions.count(), 1)
