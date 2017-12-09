from django.db import models
from .greeklit import TEXT_GROUPS, WORKS

class Lemma(models.Model):

    text = models.CharField(max_length=100, unique=True)


class Definition(models.Model):

    lemma = models.ForeignKey(Lemma, related_name="definitions")
    shortdef = models.TextField()
    source = models.CharField(max_length=100)


class TextEdition(models.Model):
    cts_urn = models.CharField(max_length=250, unique=True)
    is_core = models.BooleanField(default=False)

    def text_group_urn(self):
        parts = self.cts_urn.split(":")
        return ":".join(parts[0:3]) + ":" + parts[3].split(".")[0]

    def text_group_label(self):
        return TEXT_GROUPS.get(self.text_group_urn(), "unknown")

    def work_label(self):
        parts = self.cts_urn.split(":")
        work_urn = ":".join(parts[0:3]) + ":" + ".".join(parts[3].split(".")[0:2])
        return WORKS.get(work_urn, "unknown")


class PassageLemma(models.Model):
    text_edition = models.ForeignKey(TextEdition, related_name="passage_lemmas")
    reference = models.CharField(max_length=100)
    lemma = models.ForeignKey(Lemma, related_name="passages")
    count = models.IntegerField()


def import_data(edition_filename, dictionary_filename, passage_lemmas_filename, source):
    editions_by_id = {}
    count = 0
    with open(edition_filename) as f:
        for line in f:
            edition_id, cts_urn = line.strip().split("|")
            text_edition, _ = TextEdition.objects.get_or_create(cts_urn=cts_urn)
            editions_by_id[edition_id] = text_edition
            count += 1
    print(f"{count} editions")
    lemmas_by_id = {}
    count = 0
    with open(dictionary_filename) as f:
        for line in f:
            lemma_id, lemma_text, shortdef = line.strip().split("|")
            lemma, _ = Lemma.objects.get_or_create(text=lemma_text)
            Definition.objects.create(
                lemma = lemma,
                shortdef = shortdef,
                source = source,
            )
            lemmas_by_id[lemma_id] = lemma
            count += 1
    print(f"{count} lemmas")
    count1 = 0
    count2 = 0
    with open(passage_lemmas_filename) as f:
        for line in f:
            passage, lemma_list = line.strip().split("|")
            edition_id, passage_ref = passage.split(":")
            lemmas = []
            for lemma_count in lemma_list.split():
                if "." in lemma_count:
                    lemma_id, lcount = lemma_count.split(".")
                    lcount = int(lcount)
                else:
                    lemma_id = lemma_count
                    lcount = 1
                PassageLemma.objects.create(
                    text_edition = editions_by_id[edition_id],
                    reference = passage_ref,
                    lemma = lemmas_by_id[lemma_id],
                    count = lcount,
                )
                count2 += 1
            count1 += 1
    print(f"{count1} passages; {count2} passage lemmas")


def mark_core(filename):
    with open(filename) as f:
        for line in f:
            text_editions = TextEdition.objects.filter(
                cts_urn__startswith=line.strip())
            if len(text_editions) == 0:
                print("couldn't find:", line.strip())
            else:
                text_edition = text_editions[0]
                text_edition.is_core = True
                text_edition.save()
