from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from . import models


class BaseListsView(ListView):
    context_object_name = "resource_lists"

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        if user_pk:
            if int(user_pk) == self.request.user.pk:
                return super().get_queryset().filter(owner=user_pk)
            else:
                raise PermissionDenied(self.request)
        return super().get_queryset().filter(owner__isnull=True)


class ReadingListsView(BaseListsView):
    model = models.ReadingList
    template_name = "resource_lists/reading_lists.html"


class VocabularyListsView(BaseListsView):
    model = models.VocabularyList
    template_name = "resource_lists/vocabulary_lists.html"


class BaseSubscriptionsListsView(ListView):
    context_object_name = "subscriptions"

    def get_queryset(self):
        user_pk = int(self.kwargs["user_pk"])
        if user_pk == self.request.user.pk:
            return super().get_queryset().filter(subscriber=user_pk)
        raise PermissionDenied(self.request)


class ReadingListsSubscriptionsView(BaseSubscriptionsListsView):
    model = models.ReadingListSubscription
    template_name = "resource_lists/reading_list_subscriptions.html"


class VocabularyListsSubscriptionsView(BaseSubscriptionsListsView):
    model = models.VocabularyListSubscription
    template_name = "resource_lists/vocabulary_list_subscriptions.html"


class BaseListDetailView(DetailView):
    pk_url_kwarg = "secret_key"
    context_object_name = "resource_list"

    def get_object(self):
        try:
            return get_object_or_404(
                self.model, secret_key=self.kwargs[self.pk_url_kwarg]
            )
        except ValidationError:
            # Also capture the exception thrown by UUIDField for any strings
            # that are not valid uuid's.
            raise Http404()


class ReadingListDetailView(BaseListDetailView):
    model = models.ReadingList
    template_name = "resource_lists/reading_list.html"


class VocabularyListDetailView(BaseListDetailView):
    model = models.VocabularyList
    template_name = "resource_lists/vocabulary_list.html"


class BaseListCloneView:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        clone = self.object.duplicate(owner=self.request.user)
        success_message = f"List cloned with secret key: {clone.secret_key}."
        messages.success(self.request, success_message)
        kwargs.update({self.pk_url_kwarg: clone.pk})
        return super().dispatch(request, *args, **kwargs)


class ReadingListCloneView(BaseListCloneView, ReadingListDetailView):
    pass


class VocabularyListCloneView(BaseListCloneView, VocabularyListDetailView):
    pass


class BaseListSubscribeView:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        subscription = self.subscription_model.objects.create(
            subscriber=self.request.user,
            resource_list=self.object
        )
        self.object.subscriptions.add(subscription)
        success_message = f"Subscribed to list: {self.object}."
        messages.success(self.request, success_message)
        return super().dispatch(request, *args, **kwargs)


class ReadingListSubscribeView(BaseListSubscribeView, ReadingListDetailView):
    subscription_model = models.ReadingListSubscription


class VocabularyListSubscribeView(BaseListSubscribeView, VocabularyListDetailView):
    subscription_model = models.VocabularyListSubscription
