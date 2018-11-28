#!/usr/bin/env python3

"""
Script for counting words in the body of TEI documents.
"""


import re
import os
import glob
from lxml import etree
from os.path import join

teiFolder = join("","level1", "*.xml")


def read_tei(teiFile):
    with open(teiFile, "r", encoding="utf8") as infile:
        xml = etree.parse(infile)
        namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
        etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}note", with_tail=False)
        etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}seg")
        text = xml.xpath("//tei:body//text()", namespaces=namespaces)
        text = "\n".join(text)
        text = re.sub("[ ]{2,8}", " ", text)
        text = re.sub("\n{2,8}", "\n", text)
        text = re.sub("[ \n]{2,8}", " \n", text)
        text = re.sub("\t{1,8}", "\t", text)
        text = str(text)
        return text


def count_words(text): 
    text = re.split("\W+", text)
    numwords = len(text)
    return numwords 



def main(teiFolder):
    for teiFile in glob.glob(teiFolder): 
        filename,ext = os.path.basename(teiFile).split(".")
        text = read_tei(teiFile)
        numwords = count_words(text)
        print(filename, numwords)
    
main(teiFolder)
