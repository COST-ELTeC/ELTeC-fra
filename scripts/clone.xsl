<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    exclude-result-prefixes="xs h"
    xmlns:h="http://www.w3.org/1999/xhtml" 
    xmlns:t="http://www.tei-c.org/ns/1.0"     
    xmlns="http://www.tei-c.org/ns/1.0" 
    version="2.0">
   
    <xsl:output encoding="UTF-8" exclude-result-prefixes="#all" omit-xml-declaration="yes"></xsl:output>
    <xsl:template match="processing-instruction('xml-stylesheet')"/>
    <xsl:template match="processing-instruction('xml-model')"/>
    
    
    <!-- This stylesheet removes any existing PIs and copies all existing tagging unchanged--> 

    <!-- Add templates for elements you want to change here -->
    
    
    
    <xsl:template match="* | @* | processing-instruction()">
        <xsl:copy>
            <xsl:apply-templates select="* | @* | processing-instruction() | comment() | text()"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="text()">
        <xsl:value-of select="."/>
        <!-- could normalize() here -->
    </xsl:template>
</xsl:stylesheet>