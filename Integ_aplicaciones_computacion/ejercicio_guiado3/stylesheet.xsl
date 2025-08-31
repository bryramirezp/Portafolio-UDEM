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
                    <p><strong>Format:</strong> <xsl:value-of select="format"/></p>
                    <p><strong>Stock:</strong> <xsl:value-of select="stock"/></p>
                </div>
            </xsl:for-each>
        </div>

        <div class="totals">
            <h2>Price Summary</h2>
            <xsl:variable name="totalSum" select="sum(catalogue/book/price)"/>
            <p><strong>Total Catalogue Price:</strong> 
                $<xsl:value-of select="format-number($totalSum, '#,##0.00')"/>
            </p>
            
            <xsl:variable name="discountedTotal" select="$totalSum * 0.90"/>
            <p class="discount-price"><strong>Total with 10% Discount:</strong> 
                $<xsl:value-of select="format-number($discountedTotal, '#,##0.00')"/>
            </p>
        </div>
    </xsl:template>
</xsl:stylesheet>