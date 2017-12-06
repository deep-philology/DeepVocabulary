<img src="https://raw.githubusercontent.com/deep-reader/DeepReader/master/static/deep-reader-512.png" height=64 width=64>

# DeepVocabulary

This will primarily be a server that:

* models text tokens and lemmatisation mapped to glosses
* provides both API-based and HTML-based way of retrieving vocabulary lists for particular texts

See [overview](https://github.com/eldarion-client/DeepVocabulary/wiki/Overview).

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
npm install
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
npm run dev
```

Browse to http://localhost:3000/
