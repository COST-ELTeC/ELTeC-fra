"""
Topic Modeling with gensim: XML to TXT conversion.
Extracts all text within <p> in the body element of an XML file.
"""

# == Imports

import os
import glob
from os.path import join
from bs4 import BeautifulSoup as bs


# == Parameters

workdir = ""
xmlfolder = join(workdir, "xml", "")
txtfolder = join(workdir, "txt", "")


# == Functions

def extract_text(xmlfile):
    with open(xmlfile, "r", encoding="utf8") as infile:
        soup = bs(infile.read(), "html.parser")
        body = soup.find_all("body")[0]
        text = [item.string for item in body.find_all("p") if item.string]
        text = "\n".join(text)
        return text


def save_text(text, filename):
    with open(filename, "w", encoding="utf8") as outfile:
        outfile.write(text)
       
    
def main(xmlfolder, txtfolder):
    for xmlfile in glob.glob(join(xmlfolder, "*.xml")):
        textid = os.path.basename(xmlfile).split(".")[0]
        text = extract_text(xmlfile)
        filename = join(txtfolder, textid + ".txt")
        save_text(text, filename)

main(xmlfolder, txtfolder)