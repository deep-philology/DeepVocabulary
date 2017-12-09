from operator import itemgetter

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.db.models import Q, Sum

from .models import Lemma, TextEdition, PassageLemma, Definition
from .models import calc_overall_counts


def lemma_detail(request, pk):
    lemma = get_object_or_404(Lemma, pk=pk)
    filt = request.GET.get("filter")

    if filt:
        passages = lemma.passages.filter(text_edition__cts_urn=filt)
    else:
        passages = lemma.passages

    x = dict(
            lemma.passages.values_list(
                "text_edition").annotate(total=Sum("count")))

    y = TextEdition.objects.filter(pk__in=x.keys())
    editions = [
        {
            "text_edition": text_edition,
            "count": x[text_edition.pk],
        }
        for text_edition in y
    ]
    text_groups = {}
    for edition in editions:
        text_groups.setdefault(
            (edition["text_edition"].text_group_urn(),
            edition["text_edition"].text_group_label()),
            []).append(edition)

    corpus_freq, core_freq = lemma.frequencies()

    return render(request, "deep_vocabulary/lemma_detail.html", {
        "object": lemma,
        "filter": filt,
        "editions_count": len(editions),
        "text_groups": text_groups,
        "passages": passages,
        "corpus_freq": corpus_freq,
        "core_freq": core_freq,
    })


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
                "frequency": round(10000 * passage_lemmas[lemma_id] / total, 1),
            }
            for lemma_id in passage_lemmas.keys()
        ], key=itemgetter("count"), reverse=True
    )

    return render(request, "deep_vocabulary/word_list.html", {
        "text_edition": text_edition,
        "vocabulary": vocabulary,
        "token_total": total,
    })


def word_list_by_ref(request, cts_urn, ref_prefix):
    text_edition = get_object_or_404(TextEdition, cts_urn=cts_urn)

    if ref_prefix[-1] == "*":
        ref_filter = Q(reference__startswith=ref_prefix[:-1])
    else:
        ref_filter = Q(reference=ref_prefix)

    passage_lemmas = dict(
        PassageLemma.objects.filter(
            Q(text_edition=text_edition),
            ref_filter,
        ).values_list("lemma").annotate(total=Sum("count")))
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
                "frequency": int(100000 * passage_lemmas[lemma_id] / total) / 10,
            }
        for lemma_id in passage_lemmas.keys()
        ], key=itemgetter("count"), reverse=True
    )

    return render(request, "deep_vocabulary/word_list.html", {
        "text_edition": text_edition,
        "ref_prefix": ref_prefix,
        "vocabulary": vocabulary,
        "token_total": total,
    })
