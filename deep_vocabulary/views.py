from operator import itemgetter

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.db.models import Sum

from .models import Lemma, TextEdition, PassageLemma, Definition


class LemmaDetail(DetailView):

    model = Lemma


def lemma_by_text(request, text):
    lemma = get_object_or_404(Lemma, text=text)
    return redirect("lemma_detail", pk=lemma.pk)


def word_list_by_work(request, cts_urn):
    text_edition = get_object_or_404(TextEdition, cts_urn=cts_urn)
    passage_lemmas = dict(
        PassageLemma.objects.filter(
            text_edition=text_edition).values_list(
                "lemma").annotate(total=Sum("count")))
    definitions = dict(
        Definition.objects.filter(
            source="logeion_002", lemma__in=passage_lemmas.keys()).values_list(
                "lemma_id", "shortdef"))
    lemma_text = dict(
        Lemma.objects.filter(
            pk__in=passage_lemmas.keys()).values_list(
                "pk", "text"))
    total = sum(passage_lemmas.values())
    vocabulary = sorted(
        [
            {
                "lemma_id": lemma_id,
                "lemma_text": lemma_text[lemma_id],
                "shortdef": definitions[lemma_id],
                "count": passage_lemmas[lemma_id],
                "frequency": int(1000000 * passage_lemmas[lemma_id] / total) / 10,
            }
        for lemma_id in passage_lemmas.keys()
        ], key=itemgetter("count"), reverse=True
    )

    return render(request, "deep_vocabulary/word_list.html", {
        "text_edition": text_edition,
        "vocabulary": vocabulary,
    })
