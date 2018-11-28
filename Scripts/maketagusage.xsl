<xsl:stylesheet 
 xmlns:tei="http://www.tei-c.org/ns/1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:rng="http://relaxng.org/ns/structure/1.0"
  version="2.0">

<xsl:output method="xml"/>
<xsl:key name="TAGLIST1" match="tei:text//*" use="name(.)"/>
<xsl:key name="TAGLIST2" match="tei:teiHeader//*" use="name(.)"/>
  
<xsl:template match="/">
  <xsl:variable name="HERE" select="."/>
  <tagsDecl>
    <xsl:comment>Tags used in text</xsl:comment>
    <xsl:for-each select="distinct-values(descendant::tei:text//*/name())">
      <xsl:sort/>
      <xsl:variable name="me" select="."/>
      <xsl:for-each select="$HERE">
	<xsl:variable name="n">
	  <xsl:value-of select="count(key('TAGLIST1',$me))"/>
	</xsl:variable>
	<xsl:if test="$n &gt; 0">
	  <tagUsage>
	    <xsl:attribute name="gi">
	      <xsl:value-of select="$me"/>
	    </xsl:attribute>
	    <xsl:attribute name="occurs">
	      <xsl:value-of select="$n"/>
	    </xsl:attribute>
	  </tagUsage>
	</xsl:if>
      </xsl:for-each>
    </xsl:for-each>
  
    <xsl:comment>Tags used in teiHeader</xsl:comment>
    <xsl:for-each select="distinct-values(descendant::tei:teiHeader//*/name())">
      <xsl:sort/>
      <xsl:variable name="me" select="."/>
      <xsl:for-each select="$HERE">
        <xsl:variable name="n">
          <xsl:value-of select="count(key('TAGLIST2',$me))"/>
        </xsl:variable>
        <xsl:if test="$n &gt; 0">
          <tagUsage>
            <xsl:attribute name="gi">
              <xsl:value-of select="$me"/>
            </xsl:attribute>
            <xsl:attribute name="occurs">
              <xsl:value-of select="$n"/>
            </xsl:attribute>
          </tagUsage>
        </xsl:if>
      </xsl:for-each>
    </xsl:for-each>
  
  
  </tagsDecl>
</xsl:template>
</xsl:stylesheet>







