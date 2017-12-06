from django.views.generic import DetailView
from .models import Lemma


class LemmaDetail(DetailView):

    model = Lemma
