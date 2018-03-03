import uuid

from django.conf import settings
from django.contrib.admin.utils import NestedObjects
from django.db import models, IntegrityError
from django.db.models.fields.related import ForeignKey
from django.urls import reverse


class AuditedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CloneableModel(models.Model):
    class Meta:
        abstract = True

    def _build_graph(self):
        graph = {}
        for key in self.related_models:
            pks = [item.pk for item in self.collector.data[key]]
            items = [item for item in self.collector.data[key]]
            graph.update({
                key: dict(zip(pks, items))
            })
        return graph

    def duplicate(self, owner):  # noqa
        root_obj = None
        original_secret_key = self.secret_key

        self.collector = NestedObjects(using="default")
        self.collector.collect([self])
        self.collector.sort()
        self.related_models = self.collector.data.keys()
        graph = self._build_graph()

        for model in self.related_models:
            fks = []
            for field in model._meta.fields:
                if isinstance(field, ForeignKey) and \
                        field.remote_field.model in self.related_models:
                    fks.append(field)

            sub_objects = self.collector.data[model]
            for obj in sub_objects:
                for fk in fks:
                    fk_value = getattr(obj, f"{fk.name}_id")
                    fk_rel_to = graph[fk.remote_field.model]
                    if fk_value in fk_rel_to:
                        dupe_obj = fk_rel_to[fk_value]
                        setattr(obj, fk.name, dupe_obj)

                obj.id = None
                obj.pk = None
                cloned_from = self._meta.model.objects.get(
                    secret_key=original_secret_key
                )
                if root_obj is None:
                    root_obj = obj
                    root_obj.save(owner, cloned_from, cloned=True)
                else:
                    obj.save()

        return root_obj


class BaseList(models.Model):
    owner = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    cloned_from = models.ForeignKey(
        "self", null=True, editable=False, on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    secret_key = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title} - {self.secret_key}"

    def save(self, owner=None, cloned_from=None, cloned=False, *args, **kwargs):
        if cloned:
            self.owner = owner
            self.cloned_from = cloned_from
            self.secret_key = uuid.uuid4()
        super().save(*args, **kwargs)


class BaseListEntry(models.Model):
    note = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class BaseSubscription(models.Model):
    subscriber = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._meta.model.objects.filter(
            resource_list=self.resource_list,
            subscriber=self.subscriber
        ).exists():
            raise IntegrityError("Duplicate subscription.")
        else:
            super().save(*args, **kwargs)


class ReadingList(AuditedModel, CloneableModel, BaseList):
    class Meta:
        verbose_name = "reading list"

    def get_absolute_url(self):
        return reverse("reading_list", kwargs={"secret_key": self.secret_key})


class VocabularyList(AuditedModel, CloneableModel, BaseList):
    class Meta:
        verbose_name = "vocabulary list"

    def get_absolute_url(self):
        return reverse("reading_list", kwargs={"secret_key": self.secret_key})


class ReadingListEntry(AuditedModel, BaseListEntry):
    cts_urn = models.CharField(max_length=250)
    resource_list = models.ForeignKey(
        "resource_lists.ReadingList", related_name="entries"
    )

    class Meta:
        verbose_name = "reading list entry"
        verbose_name_plural = "reading list entries"
        order_with_respect_to = "resource_list"

    def __str__(self):
        return self.cts_urn


class VocabularyListEntry(AuditedModel, BaseListEntry):
    resource_list = models.ForeignKey(
        "resource_lists.VocabularyList", related_name="entries"
    )

    class Meta:
        verbose_name = "vocabulary list entry"
        verbose_name_plural = "vocabulary list entries"
        order_with_respect_to = "resource_list"


class ReadingListSubscription(AuditedModel, BaseSubscription):
    resource_list = models.ForeignKey(
        "resource_lists.ReadingList", related_name="subscriptions"
    )

    class Meta:
        verbose_name = "reading list subscription"
        verbose_name_plural = "reading list subscriptions"


class VocabularyListSubscription(AuditedModel, BaseSubscription):
    resource_list = models.ForeignKey(
        "resource_lists.VocabularyList", related_name="subscriptions"
    )

    class Meta:
        verbose_name = "vocabulary list subscription"
        verbose_name_plural = "vocabulary list subscriptions"
