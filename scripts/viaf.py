#!/usr/bin/env python3

"""
Script for getting data from viaf.org.
"""


# === Import statements ===

import re
import os
import glob
from lxml import etree
from os.path import join
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


# === Parameters ===

teiFolder = join("","level1", "*.xml")


# === Functions ===

def get_ids(teiFile):
    """
    Open and read the XML-TEI file and find the VIAF ID of the author
    and the XML ID of the file itself.
    """
    with open(teiFile, "r", encoding="utf8") as infile:
        xml = etree.parse(infile)
        namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
        try: 
            viafid = xml.xpath("//tei:author/tei:idno/text()", namespaces=namespaces)[0]
        except: 
            viafid = "NA"
        try: 
            xmlid = xml.xpath("//tei:TEI/@xml:id", namespaces=namespaces)[0]
        except: 
            xmlid = "NA"
        return viafid, xmlid


def get_viafrdf(authorid): 
    """
    Using the VIAF ID, get the RDF data about the author from viaf.org.
    """
    url = "http://viaf.org/viaf/" + authorid + "/rdf.xml"
    #print(url)
    response = requests.get(url)
    viafrdf = response.text
    return viafrdf



def extract_authordata(viafrdf): 
    """
    From the RDF data, extract the date of birth and death.
    """
    viafsoup = bs(viafrdf, 'xml')
    try:
        birth = viafsoup.find("schema:birthDate").string
    except: 
        birth = "NA"
    try: 
        death = viafsoup.find("schema:deathDate").string
    except: 
        death = "NA"
    return birth, death


def extract_authorname(viafrdf): 
    """
    From the RDF data, extract the name of the author.
    """
    viafsoup = bs(viafrdf, 'xml')
    try: 
        for line in viafrdf.split("\n"): 
            if "prefLabel xml:lang=\"fr-FR\"" in line:
                name = re.findall(">(.*?)<", line)[0]
        ### === For some reason, the below two solutions don't work === 
        #name = viafsoup.select('skos:prefLabel[xml:lang="fr-FR"]').string
        #name = viafsoup.findall("skos:prefLabel", {"xml:lang": "fr-FR"}).string
        #namespaces = {'skos':'http://www.w3.org/2004/02/skos/core#'}
        #name = viafrdf.xpath("//skos:prefLabel[@xml:lang='fr-FR']/text()", namespaces=namespaces)
        print("1")
        return name
    except: 
        try: 
            name = viafsoup.find("skos:prefLabel").string
            name = re.sub("\d\d\d\d-\d\d\d\d", "", name)
            name = re.sub("[\x98|\x9c|\.]", "", name)
            name = re.sub(", $", "", name)
            name = re.sub(" $", "", name)
            print("2")
            return name
        except: 
            name ="NA"
            print("3")
            return name


def merge_authordata(birth, death, name, viafid, xmlid, filename): 
    """
    Merge the data into a dictionary.
    """
    authordata = {"viaf" : viafid, "birth" : birth, "death" : death, "name": name, "xmlid":xmlid, "filename":filename}
    print(authordata)
    return authordata


def save_authordata(allauthordata): 
    """
    Save all authordata to a CSV file. 
    """
    allauthordata = pd.DataFrame(allauthordata)
    #print(allauthordata)
    with open("authordata.csv", "w", encoding="utf8") as outfile: 
        allauthordata.to_csv(outfile)


# === Coordinating function ===

def main(teiFolder):
    """
    From a collection of XML-TEI files with VIAF author identifiers,
    create a CSV file with some metadata about the authors.
    """
    allauthordata = []
    for teiFile in glob.glob(teiFolder): 
        filename,ext = os.path.basename(teiFile).split(".")
        viafid, xmlid = get_ids(teiFile)
        viafrdf = get_viafrdf(viafid)
        birth, death = extract_authordata(viafrdf)
        name = extract_authorname(viafrdf)
        authordata = merge_authordata(birth, death, name, viafid, xmlid, filename)
        allauthordata.append(authordata)
    save_authordata(allauthordata)
    
main(teiFolder)
