# imports
import re
import os
from os.path import join
import glob

# parameters
filenames = join("level1", "*l0.xml")

# functions 

def read_file(filename): 
    with open(filename, "r", encoding="utf8") as infile: 
        text = infile.read()
        return text


def fix_linebreaks(text):
    """
    Replace faulty (superfluous) paragraph separations (</p>\n<p>). 
    Replacement goes from specific to more general for best results.
    """
    # If the line is around 70 letters long and has a dot at the end, replace.
    text = re.sub("<p>(.{68,72}\.)</p>\n        <p>([A-Z])", "<p>\\1 \\2", text)       
    # If there are three dots at the end and small letters at the beginning, replace.
    text = re.sub("(\.\.\.)</p>\n        <p>([a-z])", "\\1 \\2", text)       
    # If there is an abbreviation at the end of the line, replace.
    text = re.sub("(M\.)</p>\n        <p>([A-Z])", "\\1 \\2", text)       
    # most general case (comes last)
    text = re.sub("([\w;,:])</p>\n        <p>(\w)", "\\1 \\2", text)    
    return text


def clean_text(text): 
    text = re.sub("_(.+?)_", "<emph>\\1</emph>", text)
    return text


def save_file(text, newfilename): 
    with open(newfilename, "w", encoding="utf8") as outfile: 
        outfile.write(text)
        print("done")
    


# main

def main(filenames): 
    for filename in glob.glob(filenames): 
        text = read_file(filename)
        text = fix_linebreaks(text)
        text = clean_text(text)
        newfilename = join("level1", os.path.basename(filename).split(".")[0]+"_lb.xml")
        save_file(text, newfilename)

main(filenames)
