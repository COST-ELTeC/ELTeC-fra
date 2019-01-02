# Scripts

The scripts here assume a Unix or similar working environment with the following software installed:

- Gnu Make
- saxon (XSLT processor)
- jing (XML validator)

In addition, it assumes you have local copies of :

- the ELTeC-fra repository
- the ELTEc schemas (from distantreading.github.io/Schema)

The Makefile provided will do the following:

- build a driver file to enable you to process all the files in the Orig directory as a single TEI corpus
- process the resulting corpus to list all the TEI tags used
- convert each file from CLiGs format to ELTeC level1
- validate each file against the ELTeC level-1 schema

Before running it, you will need to edit the Makefile to match the path names on your system.

To simply do the conversion and validate the results, do

`make convert validate`

You can of course use the supplied XSLT stylesheets to do the same operations in oXygen or any other XML processing environment.  

Lou Burnard, 28 oct 2018



