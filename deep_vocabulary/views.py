from operator import itemgetter

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView

from .querysets import Q_by_ref
from .models import Lemma, TextEdition, PassageLemma, Definition
from .models import calc_overall_counts

from .utils import strip_accents


def lemma_list(request):

    query = request.GET.get("q")
    order = request.GET.get("o")
    mincore = request.GET.get("mincore")
    maxcore = request.GET.get("maxcore")
    page = request.GET.get("page")

    if mincore:
        try:
            mincore = float(mincore)
        except ValueError:
            mincore = None
    if maxcore:
        try:
            maxcore = float(maxcore)
        except ValueError:
            maxcore = None

    if query:
        query = strip_accents(query)
        if query.startswith("*"):
            lemma_list = Lemma.objects.filter(unaccented__endswith=query[1:])
        elif query.endswith("*"):
            lemma_list = Lemma.objects.filter(unaccented__startswith=query[:-1])
        else:
            lemma_list = Lemma.objects.filter(unaccented=query)
    else:
        lemma_list = Lemma.objects

    corpus_total, core_total = calc_overall_counts()

    if mincore:
        lemma_list = lemma_list.filter(core_count__gte=mincore * core_total / 10000)
    if maxcore:
        lemma_list = lemma_list.filter(core_count__lte=maxcore * core_total / 10000)


    lemma_list = lemma_list.order_by({
        "1": "-core_count",
        "2": "-corpus_count",
        "3": "text",
    }.get(order, "-core_count"))

    paginator = Paginator(lemma_list, 100)

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
        editions = TextEdition.objects.filter(is_core=True).order_by("cts_urn")
    else:
        editions = TextEdition.objects.order_by("cts_urn")

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
        passages = lemma.passages.filter(text_edition__cts_urn=filt).order_by_ref()
        filtered_edition = TextEdition.objects.filter(cts_urn=filt).first()
    else:
        passages = lemma.passages.all()
        filtered_edition = None

    lemma_counts_per_edition = dict(
            lemma.passages.values_list(
                "text_edition").annotate(total=Sum("count")))

    corpus_freq, core_freq = lemma.frequencies()

    editions = [
        {
            "text_edition": text_edition,
            "lemma_count": lemma_counts_per_edition[text_edition.pk],
            "frequency": round(10000 * lemma_counts_per_edition[text_edition.pk] / text_edition.token_count, 1),
            "ratio": (
                (10000 * lemma_counts_per_edition[text_edition.pk] / text_edition.token_count) / core_freq
            ) if core_freq != 0 else None,
        }
        for text_edition in TextEdition.objects.filter(
            pk__in=lemma_counts_per_edition.keys()
        )
    ]
    text_groups = {}
    for edition in editions:
        text_groups.setdefault(
            (edition["text_edition"].text_group_urn(),
            edition["text_edition"].text_group_label()),
            []).append(edition)

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


def word_list(request, cts_urn, ref_prefix=None):
    text_edition = get_object_or_404(TextEdition, cts_urn=cts_urn)

    order = request.GET.get("o")
    mincore = request.GET.get("mincore")
    maxcore = request.GET.get("maxcore")

    corpus_total, core_total = calc_overall_counts()

    min_core_count = 0
    if mincore:
        try:
            mincore = float(mincore)
            min_core_count = mincore * core_total / 10000
        except ValueError:
            mincore = None
    max_core_count = 10000000
    if maxcore:
        try:
            maxcore = float(maxcore)
            max_core_count = maxcore * core_total / 10000
        except ValueError:
            maxcore = None

    if ref_prefix:
        if "-" in ref_prefix:
            start, end = ref_prefix.split("-")
            ref_filter = Q_by_ref(start, "gte") & Q_by_ref(end, "lte")
        else:
            ref_filter = Q_by_ref(ref_prefix)
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

    if order == "2":  # log ratio descending
        sort_key = lambda x: x["ratio"] if x["ratio"] else 1
        sort_reverse = True
    elif order == "3":  # log ratio ascending
        sort_key = lambda x: x["ratio"] if x["ratio"] else 1
        sort_reverse = False
    else:  # usually "1" but also default: count descending
        sort_key = itemgetter("count")
        sort_reverse = True


    vocabulary = sorted(
        [
            {
                "lemma_id": lemma_id,
                "lemma_text": lemma_data[lemma_id][0],
                "shortdef": definitions[lemma_id],
                "count": passage_lemmas[lemma_id],
                "frequency": round(10000 * passage_lemmas[lemma_id] / total, 1),
                "corpus_frequency": round(10000 * lemma_data[lemma_id][1] / corpus_total, 3),
                "core_frequency": round(10000 * lemma_data[lemma_id][2] / core_total, 2),
                "ratio": (
                    passage_lemmas[lemma_id] / total) / (lemma_data[lemma_id][2] / core_total
                ) if (not ref_prefix and lemma_data[lemma_id][2] != 0 and passage_lemmas[lemma_id] > 1) else None,
            }
        for lemma_id in passage_lemmas.keys()
        if min_core_count <= lemma_data[lemma_id][2] <= max_core_count
        ], key=sort_key, reverse=sort_reverse
    )

    return render(request, "deep_vocabulary/word_list.html", {
        "text_edition": text_edition,
        "ref_prefix": ref_prefix,
        "vocabulary": vocabulary,
        "token_total": total,
    })
