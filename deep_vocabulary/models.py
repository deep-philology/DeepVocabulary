from django.db import models


class Lemma(models.Model):

    text = models.CharField(max_length=100, unique=True)


class Definition(models.Model):

    lemma = models.ForeignKey(Lemma, related_name="definitions")
    shortdef = models.TextField()
    source = models.CharField(max_length=100)


class TextEdition(models.Model):
    cts_urn = models.CharField(max_length=250, unique=True)


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
