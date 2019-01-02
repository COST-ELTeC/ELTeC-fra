#!/usr/bin/env python3

"""
Script (a) for building a metadata table from ELTeC XML-TEI 
and (b) for creating some basic corpus composition statistics.

The XML-TEI files need to be valid against the ELTeC level1 schema.

Requirements: This script runs in Thonny, https://thonny.org/,
if the packages pandas and lxml are installed via the package manager.
Advanced users of Python will know how to get it to work in their preferred environment. 

Usage: The only parameter you should need to adjust is the path
encoded in the variable "teiFolder" (line 47).
Advanced users may want to change the XPath expressions to match their TEI encoding.

Normally, the script assumes that it is itself located in a folder inside the
top-level "ELTeC-xyz" folder, but it does not matter what this folder is called.
It will create a folder called "Metadata", also in the top-level folder.

Output: The script writes three files to the output folder "Metadata":
- A CSV file called "metadata.csv" with some basic metadata about the texts included in the collection
- A file called "report_corpus.txt" with a simple JSON-style string with information
about the corpus composition criteria for ELTeC collections.
- A file called "report_full.txt" with a simple JSON-style string that has some more,
maybe less universally useful information about the files.

Please send feedback to Christof at "schoech@uni-trier.de". 
"""




# === Import statements ===

import os
import re
import glob
from os.path import join
from os.path import basename
import pandas as pd
from lxml import etree


# === Path parameters ===

workingDir = join("..", "..", "ELTeC-fra")
teiFolder = join(workingDir, "level1", "*.xml")
metadataFolder = join(workingDir, "metadata")


# === XPath and output parameters ===

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


def get_metadatum(xml, xpath): 
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
        name = re.search("(.*?) \(", authordata).group(1)
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
    #pp.pprint(report)
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
    #pp.pprint(report)
    return report



def visualize_gender(fullreport): 
    import pygal
    from pygal.style import CleanStyle
    data = fullreport["au-gender"]
    #print(data)
    plot = pygal.Pie(inner_radius=.4, 
        style = CleanStyle,
        print_values = True,
        show_legend = True,
        legend_at_bottom = True,
        legend_at_bottom_columns = 3,
        title = "Number of novels per author gender")
    plot.add("Male", data["M"])
    plot.add("Female", data["F"])
    try: 
        plot.add("Other", data["X"])
    except: 
        plot.add("Other", 0)
    plot.render_to_file(join("..", "metadata", "viz_au-genders.svg"))


def visualize_sizeCat(fullreport): 
    import pygal
    from pygal.style import CleanStyle
    data = fullreport["sizeCats"]
    #print(data)
    plot = pygal.Bar(style = CleanStyle,
        print_values = True,
        show_legend = True,
        legend_at_bottom = True,
        legend_at_bottom_columns = 3,
        title = "Number of novels per size category")
    plot.add("short (10-50k words)", data["short"])
    plot.add("medium (50-100k words)", data["medium"])
    plot.add("long (>100k words)", data["long"])
    plot.render_to_file(join("..", "metadata", "viz_sizeCats.svg"))
    

def visualize_timeSlot(fullreport): 
    import pygal
    from pygal.style import CleanStyle
    data = fullreport["timeSlots"]
    #print(data)
    plot = pygal.Bar(style = CleanStyle,
        print_values = True,
        show_legend = True,
        legend_at_bottom = True,
        legend_at_bottom_columns = 4,
        title = "Number of novels per time period")
    plot.add("T1 (1840-1859)", data["T1"])
    plot.add("T2 (1860-1879)", data["T2"])
    plot.add("T3 (1880-1899)", data["T3"])
    plot.add("T4 (1900-1919)", data["T4"])
    plot.render_to_file(join("..", "metadata", "viz_timeSlots.svg"))
    

def visualize_canonicity(fullreport): 
    import pygal
    from pygal.style import CleanStyle
    data = fullreport["canonicity"]
    #print(data)
    plot = pygal.Bar(style = CleanStyle,
        print_values = True,
        show_legend = True,
        legend_at_bottom = True,
        legend_at_bottom_columns = 3,
        title = "Number of novels per canonicity category")
    try: 
        plot.add("low canonicity", data["low"])
    except: 
        plot.add("low canonicity", 0)
    plot.add("medium canonicity", data["medium"])
    try: 
        plot.add("high canonicity", data["high"])
    except: 
        plot.add("high canonicity", 0)
    plot.render_to_file(join("..", "metadata", "viz_canonicity.svg"))


def visualize_novelsperauthor(fullreport): 
    import pygal
    from pygal.style import CleanStyle
    data = fullreport["aus-per-textcount"]
    print(data)
    plot = pygal.Bar(style = CleanStyle,
        print_values = True,
        show_legend = True,
        legend_at_bottom = True,
        legend_at_bottom_columns = 5,
        title = "Number of authors with given number of novels")
    plot.add("1 novel", data[1])
    plot.add("2 novels", data[2])
    plot.add("3 novels", data[3])
    try: 
        plot.add("4 novels", data[4])
    except: 
        plot.add("4 novels", 0)
    try: 
        plot.add("5 novels", data[5])
    except: 
        plot.add("5 novels", 0)
    plot.render_to_file(join("..", "metadata", "viz_novels-per-author.svg"))





# === Coordinating function ===

def main(teiFolder, metadataFolder, xpaths, ordering):
    """
    From a collection of ELTeC XML-TEI files,
    create a CSV file with some metadata about each file.
    """
    if not os.path.exists(metadataFolder):
        os.makedirs(metadataFolder)
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
                metadatum = get_metadatum(xml, xpath)
                keys.append(key)
                metadata.append(metadatum)
            allmetadata.append(dict(zip(keys, metadata)))
        save_metadata(allmetadata, metadataFolder, ordering)
    balancereport = build_balancereport(allmetadata)
    save_report(balancereport, join(metadataFolder, "report_composition.txt"))
    fullreport = build_fullreport(allmetadata)
    save_report(fullreport, join(metadataFolder, "report_full.txt"))
    visualize_gender(fullreport)
    visualize_sizeCat(fullreport)
    visualize_timeSlot(fullreport)
    visualize_canonicity(fullreport)
    visualize_novelsperauthor(fullreport)
    
main(teiFolder, metadataFolder, xpaths, ordering)
