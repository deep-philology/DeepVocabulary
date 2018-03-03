from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import resolve
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View

from . import models


class BaseListsView(ListView):
    context_object_name = "resource_lists"

    def get_queryset(self):
        self.user_pk = self.kwargs.get("user_pk")
        if self.user_pk:
            if int(self.user_pk) == self.request.user.pk:
                return super().get_queryset().filter(owner=self.user_pk)
            else:
                raise PermissionDenied(self.request)
        return super().get_queryset().filter(owner__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.user_pk:
            context.update({"all_lists": True})
        return context


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


class ResourceListBase:
    pk_url_kwarg = "secret_key"

    def get_object(self):
        try:
            return get_object_or_404(
                self.model, secret_key=self.kwargs[self.pk_url_kwarg]
            )
        except ValidationError:
            # Also capture the exception thrown by UUIDField for any strings
            # that are not valid uuid's.
            raise Http404()


class BaseListDetailView(ResourceListBase, DetailView):
    context_object_name = "resource_list"


class ReadingListDetailView(BaseListDetailView):
    model = models.ReadingList
    template_name = "resource_lists/reading_list.html"


class VocabularyListDetailView(BaseListDetailView):
    model = models.VocabularyList
    template_name = "resource_lists/vocabulary_list.html"


class BaseListCloneView(ResourceListBase, View):
    def dispatch(self, request, *args, **kwargs):
        request.method = "POST"
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        clone = self.object.duplicate(owner=self.request.user)
        success_message = f"List cloned with secret key: {clone.secret_key}."
        messages.success(self.request, success_message)
        return HttpResponseRedirect(clone.get_absolute_url())


class ReadingListCloneView(BaseListCloneView):
    model = models.ReadingList


class VocabularyListCloneView(BaseListCloneView):
    model = models.VocabularyList


class BaseListSubscribeView(ResourceListBase, View):
    def dispatch(self, request, *args, **kwargs):
        request.method = "POST"
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_url = resolve(request.path_info).url_name
        if current_url.endswith("list_subscribe"):
            return self.subscribe(request, *args, **kwargs)
        else:
            return self.unsubscribe(request, *args, **kwargs)

    def subscribe(self, request, *args, **kwargs):
        if self.subscription_model.objects.filter(
            subscriber=self.request.user, resource_list=self.object
        ).exists():
            message = f"User {self.request.user} is already subscribed to {self.object}."
            messages.warning(self.request, message)
        else:
            subscription = self.subscription_model.objects.create(
                subscriber=self.request.user,
                resource_list=self.object
            )
            self.object.subscriptions.add(subscription)
            message = f"Subscribed to {self.object}."
            messages.success(self.request, message)
        return HttpResponseRedirect(self.object.get_absolute_url())

    def unsubscribe(self, request, *args, **kwargs):
        if not self.subscription_model.objects.filter(
            subscriber=self.request.user, resource_list=self.object
        ).exists():
            message = f"User {self.request.user} is not subscribed to {self.object}."
            messages.warning(self.request, message)
        else:
            self.subscription_model.objects.get(
                subscriber=self.request.user,
                resource_list=self.object
            ).delete()
            message = f"Unsubscribed from {self.object}."
            messages.success(self.request, message)
        return HttpResponseRedirect(self.object.get_absolute_url())


class ReadingListSubscribeView(BaseListSubscribeView):
    model = models.ReadingList
    subscription_model = models.ReadingListSubscription


class VocabularyListSubscribeView(BaseListSubscribeView):
    model = models.VocabularyList
    subscription_model = models.VocabularyListSubscription
