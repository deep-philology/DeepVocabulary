from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from .views import LemmaDetail, lemma_by_text


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),

    url(r"^lemma/(?P<pk>\d+)/$", LemmaDetail.as_view(), name="lemma_detail"),
    url(r"^lemma/text/(?P<text>[^/]+)/$", lemma_by_text, name="lemma_by_text"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
