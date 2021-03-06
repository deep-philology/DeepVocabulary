<img src="https://raw.githubusercontent.com/deep-reader/DeepReader/master/static/deep-reader-512.png" height=64 width=64>

# DeepVocabulary

This will primarily be a server that:

* models text tokens and lemmatisation mapped to glosses
* provides both API-based and HTML-based way of retrieving vocabulary lists for particular texts

See [overview](https://github.com/eldarion-client/DeepVocabulary/wiki/Overview).

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```shell
createdb deep-vocabulary
npm install
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
python manage.py shell
```

In the Python shell:

```python
from deep_vocabulary.models import *
import_data("./data/editions_03.txt", "./data/logeion_03.txt", "./data/bag_of_words_03.txt", "logeion_003")
mark_core("./data/core_works_urn.txt")
update_lemma_counts()
update_edition_token_counts()
update_lemma_unaccented()
update_lemma_sort_keys()
```

Some of the Python shell commands take a few minutes (especially `import_data`, `update_lemma_counts`, and `update_lemma_sort_keys`). `mark_core` may report some URNs could not be found; this can be ignored.

Once the above has been run,

```shell
npm run dev
```

and browse to http://localhost:3000/
