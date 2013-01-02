#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs

import optparse
import re
import csv
import xml.etree.cElementTree as etree


#iso639={"de":["Wikipedia:", "Hilfe:", "Datei:", "Portal:", "MediaWiki:", "Vorlage:", "Kategorie:"],
#        "en":["Wikipedia:", "Hilfe:", "Datei:", "Portal:", "MediaWiki:", "Vorlage:", "Kategorie:"],
#        "ru":["Wikipedia:", "Hilfe:", "Datei:", "Portal:", "MediaWiki:", "Vorlage:", "Kategorie:"]}

def generatedict(infile,outfile,lang, excfile):

    pattern=re.compile("(?<=\[\["+lang+":).*?(?=\]\])",re.U)

    # titles of the exclude file are ignored
    exclude=[]
    if excfile:
        # http://stackoverflow.com/questions/544921/best-method-for-reading-newline-delimited-files-in-python-and-discarding-the-newl
        # http://stackoverflow.com/questions/147741/character-reading-from-file-in-python
        exclude=codecs.open(excfile,encoding="utf-8").read().splitlines()
        exclude=[word for word in exclude if word.strip()]

    out = csv.writer(outfile)

    # see http://stackoverflow.com/questions/324214/what-is-the-fastest-way-to-parse-large-xml-docs-in-python
    context=etree.iterparse(infile,events=("start","end", "start-ns"))

    # convert iterparse object into generator
    context=iter(context)

    # get the namespace (xmlns attribute in mediawiki tag)
    event,namespace = context.next()
    xmlns = namespace[1]
    print xmlns

    # skip over second namespace (xmlns:xsi attribute in mediawiki tag)
    event,namespace = context.next()
    # store root tag (mediawiki tag)
    event,root = context.next()

    # cElementTree seems to parse "xml:lang" as "{http://www.w3.org/XML/1998/namespace}lang".
    # couldn't find a better solution than below
    # How can I figure out the default mappings xml-> http://www.w3.org/XML/1998/namespace
    # cElementTree is using????
    sourcelang=root.attrib["{http://www.w3.org/XML/1998/namespace}lang"]

    # write header for csv file
    out.writerow([sourcelang+":",lang+":"])

    for event, elem in context:
        store = False

        # If at the end of a page tag ...
        if event == "end" and elem.tag == "{"+xmlns+"}"+"page":
            store = True

            # find <title> tag
            title=elem.findtext("{"+xmlns+"}"+"title")

            # If title contains one of the words from the exclude list of the sourcelanguage...
            for word in exclude:
                if word in title:
                    # do not store this article
                    store=False
                    print "Excluding :",title

            # If article is not excluded...
            if store:
                # find <revision> tag
                revision=elem.find("{"+xmlns+"}"+"revision")

                # If a <revision> tag exists ...
                if revision != None:
                    # find <text> tag
                    text=revision.findtext("{"+xmlns+"}"+"text")

                    # If <text> tag exists...
                    if text != None:
                        # search for language link
                        result=pattern.search(text)
                        # If a language link exists...
                        if result !=None:
                            print title,result.group(0)
                            # write title and translation to output file
                            out.writerow([title.encode("utf-8"),result.group(0).encode("utf-8")])

            # very important: clean up memory!
            # see http://stackoverflow.com/questions/324214/what-is-the-fastest-way-to-parse-large-xml-docs-in-python
            root.clear()


def main():
    parser = optparse.OptionParser()
    parser.usage = """A program for generating a 2-language dictionary from a wikipedia dump. The
	results are stored as CSV file, where the first column holds the wikipedia titles in the source language,
	the second one the translated titles in the destination language extracted from the interlanguage links of the article."""
    parser.add_option("-i", "--in", dest="filein", help="input wikipedia dump (XML)", metavar="INFILE")
    parser.add_option("-o", "--out", dest="fileout", help="output file (CSV)", metavar="OUTFILE")
    parser.add_option("-l", "--lang", dest="lang", help="language code (ISO 639-1) for destination language (e.g. \"de\",\"ru\",...)" , metavar="LANG")
    parser.add_option("-x", "--exclude", dest="excfile", help ="ignore titles from EXCLUDE file", metavar="EXCLUDE")

    (options, args) = parser.parse_args()

    if options.filein is None:
        parser.error("Missing input file!")

    if options.fileout is None:
        parser.error("Missing output file!")

    if options.lang is None:
        parser.error("Missing destination language code (ISO 639-1)!")
#    elif options.lang not in iso639:
#        parser.error("Unknown language code!")

    try:
        # "rb" : readable, binary file (just reading a stream of bytes, no decoding)
        filein=open(options.filein, "rb")
    except IOError:
        print "Cannot read from ", options.filein

    try:
        # "wb" : writable, binary file (just writing a stream of bytes, no encoding)
        fileout=open(options.fileout, "wb")
    except IOError:
        print "Cannot write to ", options.fileout

    generatedict(filein,fileout,options.lang, options.excfile)


if __name__ == "__main__":
    # when one "executes" a python program, it's __name__ is
    # __main__, otherwise it's name will be the module name
    main()
