#!/usr/bin/env bash

curl https://dumps.wikimedia.org/iswiktionary/latest/iswiktionary-latest-pages-articles.xml.bz2 -o articles.xml.bz2
bzip2 -d articles.xml.bz2