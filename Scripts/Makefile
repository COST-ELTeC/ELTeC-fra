ECHO=
LOCAL=/media/christof/mydata/repos/cost/
CORPUS=$(LOCAL)/ELTeC-fra
ORIG=$(CORPUS)/Orig
SCHEMA0=$(LOCAL)/distantreading.github.io/Schema/eltec-0.rng
SCHEMA1=$(LOCAL)/distantreading.github.io/Schema/eltec-1.rng
CORPUSHDR=corpHeaderStart.txt
CURRENT=`pwd`

driver:
	echo rebuild driver file for originals
	cp $(CORPUSHDR) $(ORIG)/driver.tei;\
		for f in $(ORIG)/*.xml ; do \
		echo "<xi:include href='$$f'/>" >> $(ORIG)/driver.tei; \
	done; echo "</teiCorpus>" >> $(ORIG)/driver.tei
tagusage:
	echo check tags used in originals
	saxon $(ORIG)/driver.tei maketagusage.xsl > taguse.xml 
convert:
	echo convert to eltec1 and rewrite repo
	cd $(ORIG); for f in *.xml; do \
	echo $$f; java -jar /usr/share/java/saxon9he.jar $$f ../Scripts/CLIGStoELTeC.xsl > ../level1/$$f; done; \
	cd $(CURRENT)
validate:
	echo check validity of files in repo
	cd $(CORPUS)/level1; for f in *.xml; do \
	echo $$f; jing $(SCHEMA1) $$f; done; \
	cd $(CURRENT)

# run this makefile from within Scripts directory  
