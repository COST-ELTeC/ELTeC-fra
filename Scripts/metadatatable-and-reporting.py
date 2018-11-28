#!/usr/bin/env python3

"""
Script for building a metadata table from ELTeC XML-TEI 
and for creating some basic corpus composition statistics. 
Requirement: the XML-TEI files are valid against the ELTeC level1 schema.
"""


# === Import statements ===

import re
import glob
from os.path import join
from os.path import basename
import pandas as pd
from lxml import etree


# === Parameters ===

teiFolder = join("..", "level1", "*.xml")
metadataFolder = join("..", "Metadata")

xpaths = {"xmlid" : "//tei:TEI/@xml:id", 
          "title" : "//tei:titleStmt/tei:title/text()",
          "title-ids" : "//tei:titleStmt/tei:title/@ref",
          "au-ids" : "//tei:titleStmt/tei:author/@ref",
          "numwords" : "//tei:extent/tei:measure[@unit='words']/text()",
          "au-gender" : "//tei:textDesc/eltec:authorGender/@key",
          "sizeCat" : "//tei:textDesc/eltec:size/@key",
          "canonicity" : "//tei:textDesc/eltec:canonicity/@key",
          "time-slot" : "//tei:textDesc/eltec:timeSlot/@key",
          "first-ed" : "//tei:bibl[@type='edition-first']/tei:date/text()",
          "language" : "//tei:langUsage/tei:language/@ident"}

ordering = ["filename", "xmlid", "au-name", "title", "au-birth", "au-death", "au-gender", "au-ids", "first-ed", "title-ids", "sizeCat", "canonicity", "time-slot", "numwords", "language"]


# === Functions ===


def open_file(teiFile): 
    """
    Open and parse the XML file. 
    Returns an XML tree.
    """
    with open(teiFile, "r", encoding="utf8") as infile:
        xml = etree.parse(infile)
        return xml



def get_metadatum(xml, key, xpath): 
    """
    For each metadata key and XPath defined above, retrieve the 
    metadata item from the XML tree.
    Note that the individual identifers for au-ids and title-ids 
    are not split into individual columns.
    """
    try: 
        namespaces = {'tei':'http://www.tei-c.org/ns/1.0', 'eltec':'http://distantreading.net/eltec/ns'}       
        metadatum = xml.xpath(xpath, namespaces=namespaces)[0]
    except: 
        metadatum = "NA"
    return metadatum


def get_authordata(xml): 
    """
    Retrieve the author field and split it into constituent parts.
    Expected pattern: "name (alternatename) (birth-death)"
    where birth and death are both four-digit years. 
    The alternate name is ignored. 
    Note that the first and last names are not split into separate
    entries, as this is not always a trivial decision to make.
    """
    try: 
        namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}       
        authordata = xml.xpath("//tei:titleStmt/tei:author/text()", namespaces=namespaces)[0]
        name = re.search("(.*?)\(", authordata).group(1)
        birth = re.search("\((\d\d\d\d)", authordata).group(1)
        death = re.search("(\d\d\d\d)\)", authordata).group(1)
    except: 
        name = "NA"
        birth = "NA"
        death = "NA"        
    return name,birth,death



def save_metadata(metadata, metadataFolder, ordering): 
    """
    Save all metadata to a CSV file. 
    The ordering of the columns follows the list defined above.
    """
    metadata = pd.DataFrame(metadata)
    metadata = metadata[ordering]
    with open(join(metadataFolder, "metadata.csv"), "w", encoding="utf8") as outfile: 
        metadata.to_csv(outfile)


def build_balancereport(allmetadata): 
    """
    Based on the metadata extracted in the previous steps, 
    calculate some basic corpus composition indicators. 
    """
    from collections import Counter
    allmetadata = pd.DataFrame(allmetadata)
    allmetadata = allmetadata[ordering]
    # Number of novels
    num_novels = len(set(list(allmetadata.loc[:,"xmlid"])))
    # Number of texts per time period
    time_slots = dict(Counter(list(allmetadata.loc[:,"time-slot"])))
    # Number of texts per size category
    size_cats = dict(Counter(list(allmetadata.loc[:,"sizeCat"])))
    # Number of texts per canon level
    canon_levels = dict(Counter(list(allmetadata.loc[:,"canonicity"])))
    # Number of texts per author gender
    author_genders = dict(Counter(list(allmetadata.loc[:,"au-gender"])))
    report = {"num_novels" : num_novels, 
              "timeSlots" : time_slots,
              "sizeCats" : size_cats,
              "canonicity" : canon_levels,
              "au-gender" : author_genders}
    import pprint
    pp = pprint.PrettyPrinter(indent=0, width=30, compact=True) 
    pp.pprint(report)
    return report


def save_report(report, filename): 
    with open(filename, "w", encoding="utf8") as outfile:
        outfile.write(str(report))
    

def build_fullreport(allmetadata): 
    """
    Based on the metadata extracted in the previous steps, 
    calculate some basic corpus composition indicators. 
    """
    from collections import Counter
    allmetadata = pd.DataFrame(allmetadata)
    allmetadata = allmetadata[ordering]
    # Number of novels
    num_novels = len(set(list(allmetadata.loc[:,"xmlid"])))
    # Number of authors
    num_authors = len(set(list(allmetadata.loc[:,"au-name"])))
    # Number of texts per time period
    time_slots = dict(Counter(list(allmetadata.loc[:,"time-slot"])))
    # Number of texts per size category
    size_cats = dict(Counter(list(allmetadata.loc[:,"sizeCat"])))
    # Number of texts per size category
    canon_levels = dict(Counter(list(allmetadata.loc[:,"canonicity"])))
    # Number of texts per author gender
    author_genders = dict(Counter(list(allmetadata.loc[:,"au-gender"])))
    # Number of texts per author
    texts_per_author = dict(Counter(list(allmetadata.loc[:,"au-name"])))
    # Number of authors per text-count 
    authors_per_textcount = Counter(list(texts_per_author.values()))
    # Text lengths
    text_lengths = list(allmetadata.loc[:,"numwords"])
    report = {"num_novels" : num_novels, 
              "num_authors": num_authors, 
              "timeSlots" : time_slots,
              "sizeCats" : size_cats,
              "canonicity" : canon_levels,
              "au-gender" : author_genders,
              "texts-per-au" : texts_per_author,
              "aus-per-textcount" : authors_per_textcount,
              "text_lengths" : text_lengths}
    import pprint
    pp = pprint.PrettyPrinter(indent=0, width=30, compact=True) 
    pp.pprint(report)
    return report


# === Coordinating function ===

def main(teiFolder, metadataFolder, xpaths, ordering):
    """
    From a collection of ELTeC XML-TEI files,
    create a CSV file with some metadata about each file.
    """
    allmetadata = []
    for teiFile in glob.glob(teiFolder): 
        filename,ext = basename(teiFile).split(".")
        #print(filename)
        if "schemas" not in filename:
            keys = []
            metadata = []
            keys.append("filename")
            metadata.append(filename)
            xml = open_file(teiFile)
            name,birth,death = get_authordata(xml)
            keys.extend(["au-name", "au-birth", "au-death"])
            metadata.extend([name, birth, death])
            for key,xpath in xpaths.items(): 
                metadatum = get_metadatum(xml, key, xpath)
                keys.append(key)
                metadata.append(metadatum)
            allmetadata.append(dict(zip(keys, metadata)))
        save_metadata(allmetadata, metadataFolder, ordering)
    balancereport = build_balancereport(allmetadata)
    save_report(balancereport, join(metadataFolder, "report_composition.txt"))
    fullreport = build_fullreport(allmetadata)
    save_report(fullreport, join(metadataFolder, "report_full.txt"))
    
main(teiFolder, metadataFolder, xpaths, ordering)
