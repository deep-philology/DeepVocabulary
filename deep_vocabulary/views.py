from math import log
from operator import itemgetter

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView

from .models import Lemma, TextEdition, PassageLemma, Definition
from .models import calc_overall_counts


def lemma_list(request):
    lemma_list = Lemma.objects.order_by("-core_count")
    paginator = Paginator(lemma_list, 100)

    page = request.GET.get("page")
    try:
        lemmas = paginator.page(page)
    except PageNotAnInteger:
        lemmas = paginator.page(1)
    except EmptyPage:
        lemmas = paginator.page(paginator.num_pages)

    return render(request, "deep_vocabulary/lemma_list.html", {
        "lemmas": lemmas,
    })


def editions_list(request):
    core = "core" in request.GET

    if core:
        editions = TextEdition.objects.filter(is_core=True)
    else:
        editions = TextEdition.objects.all()

    text_groups = {}

    for edition in editions:
        text_groups.setdefault(
            (edition.text_group_urn(), edition.text_group_label()), []
        ).append(edition)

    return render(request, "deep_vocabulary/editions_list.html", {
        "text_groups": text_groups,
        "core": core,
    })


def lemma_detail(request, pk):
    lemma = get_object_or_404(Lemma, pk=pk)
    filt = request.GET.get("filter")

    if filt:
        passages = lemma.passages.filter(text_edition__cts_urn=filt)
        filtered_edition = TextEdition.objects.filter(cts_urn=filt).first()
    else:
        passages = lemma.passages
        filtered_edition = None

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
        "filtered_edition": filtered_edition,
        "editions_count": len(editions),
        "text_groups": text_groups,
        "passages": passages,
        "corpus_freq": corpus_freq,
        "core_freq": core_freq,
    })


def lemma_by_text(request, text):
    lemma = get_object_or_404(Lemma, text=text)
    return redirect("lemma_detail", pk=lemma.pk)


def word_list(request, cts_urn, ref_prefix=None):
    text_edition = get_object_or_404(TextEdition, cts_urn=cts_urn)

    if ref_prefix:
        if ref_prefix[-1] == "*":
            ref_filter = Q(reference__startswith=ref_prefix[:-1])
        else:
            ref_filter = Q(reference=ref_prefix)
    else:
        ref_filter = Q()

    passage_lemmas = dict(
        PassageLemma.objects.filter(
            Q(text_edition=text_edition),
            ref_filter,
        ).values_list("lemma").annotate(total=Sum("count")))
    definitions = dict(
        Definition.objects.filter(
            source="logeion_002", lemma__in=passage_lemmas.keys()).values_list(
                "lemma_id", "shortdef"))
    lemma_values_list = Lemma.objects.filter(
            pk__in=passage_lemmas.keys()
        ).values_list(
            "pk", "text", "corpus_count", "core_count"
        )
    lemma_data = {item[0]: item[1:4] for item in lemma_values_list}
    total = sum(passage_lemmas.values())
    corpus_total, core_total = calc_overall_counts()
    vocabulary = sorted(
        [
            {
                "lemma_id": lemma_id,
                "lemma_text": lemma_data[lemma_id][0],
                "shortdef": definitions[lemma_id],
                "count": passage_lemmas[lemma_id],
                "frequency": int(100000 * passage_lemmas[lemma_id] / total) / 10,
                "corpus_frequency": round(10000 * lemma_data[lemma_id][1] / corpus_total, 1),
                "core_frequency": round(10000 * lemma_data[lemma_id][2] / core_total, 1),
                "log_ratio": round(log((passage_lemmas[lemma_id] / total) / (lemma_data[lemma_id][2] / core_total))) if not ref_prefix and lemma_data[lemma_id][2] != 0 else None,
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
