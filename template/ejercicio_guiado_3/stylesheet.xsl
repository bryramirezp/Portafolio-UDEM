<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/">
        <h1>Book Catalogue</h1>
        <div class="catalogue-container">
            <xsl:for-each select="catalogue/book">
                <div class="book-box">
                    <h2><xsl:value-of select="title"/></h2>
                    <p><strong>Author:</strong> <xsl:value-of select="author"/></p>
                    <p><strong>ISBN:</strong> <xsl:value-of select="@isbn"/></p>
                    <p><strong>Year:</strong> <xsl:value-of select="year"/></p>
                    <p><strong>Genre:</strong> <xsl:value-of select="genre"/></p> 
                    <p class="price"><strong>Price:</strong> $<xsl:value-of select="price"/></p>
            
                    <p class="individual-discount">
                        <strong>Price with 10% off:</strong> 
                        $<xsl:value-of select="format-number(price * 0.90, '#,##0.00')"/>
                    </p>

                    <p><strong>Format:</strong> <xsl:value-of select="format"/></p> 
                    <p><strong>Stock:</strong> <xsl:value-of select="stock"/></p> 
                </div>
            </xsl:for-each>
        </div>
    </xsl:template>
</xsl:stylesheet>



