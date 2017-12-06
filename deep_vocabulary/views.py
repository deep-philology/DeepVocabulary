from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView

from .models import Lemma


class LemmaDetail(DetailView):

    model = Lemma


def lemma_by_text(request, text):
    lemma = get_object_or_404(Lemma, text=text)
    return redirect("lemma_detail", pk=lemma.pk)
