from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^reading/$", views.ReadingListsView, name="all_reading_lists"),
    url(r"^reading/owner/(?P<user_pk>\d+)$", views.ReadingListsView, name="user_reading_lists"),
    url(r"^reading/(?P<pk>\d+)/$", views.ReadingListView, name="reading_list"),

    url(r"^vocabulary/$", views.VocabularyListsView, name="vocabulary_lists"),
    url(r"^vocabulary/owner/(?P<user_pk>\d+)$", views.ReadingListsView, name="user_vocabulary_lists"),
    url(r"^vocabulary/(?P<pk>\d+)/$", views.VocabularyListView, name="vocabulary_list"),
]
