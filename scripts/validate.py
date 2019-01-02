#!/usr/bin/env python3

"""
Validate an XML file against the ELTEC schema.

"""

import re
import os
import glob
from lxml import etree
from os.path import join


workdir = join("..")
xmlfolder = join(workdir, "level1", "*_*.xml")
schemafile = join(workdir, "..", "distantreading.github.io", "Schema", "eltec-1.rng")
reportfile = join(workdir, "metadata", "validation-report.txt")


def read_xml(xmlfile):
    xml = etree.parse(xmlfile)
    return xml


def read_schema(schemafile): 
    schema = etree.parse(schemafile)
    return schema


def validate(xml, schema, basename): 
    validator = etree.RelaxNG(schema)
    result = validator.validate(xml)
    if result == True: 
        report = str(basename + ":\tvalid!\n")
    else: 
        report = str(basename + ":\tNOT valid!\n" + str(validator.error_log) + "\n\n")
    return result, report


def save_txt(reportfile, report): 
    with open(reportfile, "a", encoding="utf8") as outfile: 
        outfile.write(report)


def main(xmlfolder, reportfile, schemafile):
    schema = read_schema(schemafile)
    counter = 0
    valid = 0
    for xmlfile in glob.glob(xmlfolder): 
        basename, ext = os.path.basename(xmlfile).split(".")
        counter +=1
        print("Now treating:", basename)
        xml = read_xml(xmlfile)
        result, report = validate(xml, schema, basename)
        if result == True: 
            valid +=1
        save_txt(reportfile, report)
    print("Valid files: " + str(valid) + "/" + str(counter))
    
main(xmlfolder, reportfile, schemafile)
