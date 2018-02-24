from django.contrib.auth.models import User

import factory
from factory.django import DjangoModelFactory as ModelFactory


class UserFactory(ModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"email_{n}@example.com")


class ReadingListFactory(ModelFactory):
    class Meta:
        model = "resource_lists.ReadingList"

    title = factory.Sequence(lambda n: f"reading_list_{n}")


class VocabularyListFactory(ModelFactory):
    class Meta:
        model = "resource_lists.VocabularyList"

    title = factory.Sequence(lambda n: f"vocabulary_list_{n}")
