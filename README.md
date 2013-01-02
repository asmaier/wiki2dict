Wiki2Dict
=========

This project offers some python scripts for generating a bilingual dictionary from a wikipedia dump.
The result is stored as CSV file, where the first column holds the wikipedia titles
in the source language, the second one the translated titles in the destination
language extracted from the interlanguage links of the article.

System Requirements
-------------------
Tested on Mac OS X 10.6.8 with Python 2.6.5. Needs `bash`, `bunzip2` and `curl`for downloading the
Wikipedia dump files. The scripts most probably also run on Linux, but not on Windows.

Usage
-----

1. Download the latest Wikipedia XML dump file of the source language (in the example we use german (`de`) ).
Be aware that the XML dump files from Wikipedia can be quite big (e.g. the german one is 2.8 GB), so the
download might take a while:
```
sh getwiki.sh de
```
2. Generate the dictionary (here a german-russian dictionary) into the CSV file `de_ru.csv`
excluding articles with keywords from the `dewiki-exclude.txt` file:
```
python generatedict.py -i dewiki-latest-pages-articles.xml -l ru -o de_ru.csv -x excludes/dewiki-exclude.txt
```
3. With `searchdict.py` you can search through the dictionary for a translation of a word:
```
python searchdict.py -i de_ru.csv
Enter word to translate:
```

Enjoy!


