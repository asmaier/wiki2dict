#!/bin/bash

PREFIX=$1

PAGES=http://dumps.wikimedia.org/${PREFIX}wiki/latest/${PREFIX}wiki-latest-pages-articles.xml.bz2

echo Downloading $PAGES
# -L follows redirects
curl -OL $PAGES
bunzip2 -vf `basename $PAGES`