from django.db import models


class Lemma(models.Model):

    text = models.CharField(max_length=100, unique=True)


class Definition(models.Model):

    lemma = models.ForeignKey(Lemma, related_name="definitions")
    shortdef = models.TextField()
    source = models.CharField(max_length=100)


def import_dictionary(filename, source):
    with open(filename) as f:
        for line in f:
            lemma_text, shortdef = line.strip().split("|")
            lemma, _ = Lemma.objects.get_or_create(text=lemma_text)
            Definition.objects.create(
                lemma = lemma,
                shortdef = shortdef,
                source = source,
            )
