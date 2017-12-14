import re
import unicodedata

from itertools import zip_longest


def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def chunker(iterable, n):
    args = [iter(iterable)] * n
    for chunk in zip_longest(*args, fillvalue=None):
        yield [item for item in chunk if item is not None]


def pg_array_format(iterable):
    return "{{{0}}}".format(",".join([f"\"{x}\"" for x in iterable]))


def natural_sort_key_item(ref):
    if ref is None:
        return []
    return [
        v.zfill(4) if v.isdigit() else v
        for v in filter(bool, re.split(r"(\d+)", ref))
    ]

def natural_sort_key(ref, depth):
    tree = ref.split(".")
    assert len(tree) <= depth, "too deep for database schema"
    key = natural_sort_key_item
    return tuple(map(key, next(zip_longest(*([iter(tree)] * depth)))))
