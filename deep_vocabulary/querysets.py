from django.db import models

from .utils import natural_sort_key


class PassageLemmaQuerySet(models.QuerySet):

    def filter_by_ref(self, ref):
        return self.filter(Q_by_ref(ref))

    def exclude_by_ref(self, ref):
        return self.exclude(Q_by_ref(ref))

    def order_by_ref(self, desc=False):
        dash = "-" if desc else ""
        return self.order_by(f"{dash}ref1", f"{dash}ref2", f"{dash}ref3", f"{dash}ref4")


def Q_by_ref(ref, lookup="exact"):
    kwargs = {}
    sort_key = natural_sort_key(ref, depth=4)
    for i, k in enumerate(filter(bool, sort_key)):
        kwargs[f"ref{i + 1}__{lookup}"] = k
    return models.Q(**kwargs)
