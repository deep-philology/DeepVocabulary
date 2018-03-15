from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^reading/$", views.ReadingListsView.as_view(), name="reading_lists"),
    url(r"^reading/owner/(?P<user_pk>\d+)/$",
        views.ReadingListsView.as_view(), name="user_reading_lists"),
    url(r"^reading/subscriptions/owner/(?P<user_pk>\d+)/$",
        views.ReadingListsSubscriptionsView.as_view(), name="reading_list_subscriptions"),

    url(r"^reading/(?P<secret_key>[0-9a-f-]+)/$",
        views.ReadingListDetailView.as_view(), name="reading_list"),

    url(r"^reading/create/$",
        views.ReadingListCreateView.as_view(), name="reading_list_create"),
    url(r"^reading/update/(?P<secret_key>[0-9a-f-]+)/$",
        views.ReadingListUpdateView.as_view(), name="reading_list_update"),
    url(r"^reading/delete/(?P<secret_key>[0-9a-f-]+)/$",
        views.ReadingListDeleteView.as_view(), name="reading_list_delete"),

    url(r"^reading/clone/(?P<secret_key>[0-9a-f-]+)/$",
        views.ReadingListCloneView.as_view(), name="reading_list_clone"),
    url(r"^reading/subscribe/(?P<secret_key>[0-9a-f-]+)/$",
        views.ReadingListSubscribeView.as_view(), name="reading_list_subscribe"),
    url(r"^reading/unsubscribe/(?P<secret_key>[0-9a-f-]+)/$",
        views.ReadingListSubscribeView.as_view(), name="reading_list_unsubscribe"),

    url(r"^vocabulary/$", views.VocabularyListsView.as_view(), name="vocabulary_lists"),
    url(r"^vocabulary/owner/(?P<user_pk>\d+)/$",
        views.ReadingListsView.as_view(), name="user_vocabulary_lists"),
    url(r"^vocabulary/subscriptions/owner/(?P<user_pk>\d+)/$",
        views.VocabularyListsSubscriptionsView.as_view(), name="vocabulary_list_subscriptions"),

    url(r"^vocabulary/(?P<secret_key>[0-9a-f-]+)/$",
        views.VocabularyListDetailView.as_view(), name="vocabulary_list"),

    url(r"^vocabulary/create/$",
        views.VocabularyListCreateView.as_view(), name="vocabulary_list_create"),
    url(r"^vocabulary/update/(?P<secret_key>[0-9a-f-]+)/$",
        views.VocabularyListUpdateView.as_view(), name="vocabulary_list_update"),
    url(r"^vocabulary/delete/(?P<secret_key>[0-9a-f-]+)/$",
        views.VocabularyListDeleteView.as_view(), name="vocabulary_list_delete"),

    url(r"^vocablary/clone/(?P<secret_key>[0-9a-f-]+)/$",
        views.VocabularyListCloneView.as_view(), name="vocabulary_list_clone"),
    url(r"^vocabulary/subscribe/(?P<secret_key>[0-9a-f-]+)/$",
        views.VocabularyListSubscribeView.as_view(), name="vocabulary_list_subscribe"),
    url(r"^vocabulary/unsubscribe/(?P<secret_key>[0-9a-f-]+)/$",
        views.VocabularyListSubscribeView.as_view(), name="vocabulary_list_unsubscribe"),
]
