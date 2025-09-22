<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes"/>

    <xsl:template match="/">
        <html>
            <head>
                <style>
                    .invoice-box { max-width: 800px; margin: auto; padding: 30px; border: 1px solid #eee; box-shadow: 0 0 10px rgba(0, 0, 0, 0.15); font-size: 16px; line-height: 24px; font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; color: #555; }
                    .invoice-box table { width: 100%; line-height: inherit; text-align: left; border-collapse: collapse; }
                    .invoice-box table td { padding: 5px; vertical-align: top; }
                    .invoice-box table tr td:nth-child(2) { text-align: right; }
                    .invoice-box table tr.top table td { padding-bottom: 20px; }
                    .invoice-box table tr.heading td { background: #eee; border-bottom: 1px solid #ddd; font-weight: bold; }
                    .invoice-box table tr.details td { padding-bottom: 20px; }
                    .invoice-box table tr.item td { border-bottom: 1px solid #eee; }
                    .invoice-box table tr.total td:nth-child(2) { border-top: 2px solid #eee; font-weight: bold; }
                    .right { text-align: right; }
                </style>
            </head>
            <body>
                <xsl:apply-templates select="factura"/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="factura">
        <div class="invoice-box">
            <table>
                <tr class="top">
                    <td colspan="2">
                        <table>
                            <tr>
                                <td>
                                    <h2>Joyería "El Brillo"</h2>
                                </td>
                                <td>
                                    <strong>Factura #:</strong> <xsl:value-of select="encabezado/folio"/><br/>
                                    <strong>Creada:</strong> <xsl:value-of select="encabezado/fecha"/><br/>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr class="information">
                    <td colspan="2">
                         <table>
                            <tr>
                                <td>
                                    <strong>Cliente:</strong><br/>
                                    <xsl:value-of select="cliente/nombre"/><br/>
                                    <xsl:value-of select="cliente/email"/>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr class="heading">
                    <td>Producto</td>
                    <td class="right">Precio</td>
                </tr>
                <xsl:for-each select="items/item">
                    <tr class="item">
                        <td><xsl:value-of select="nombre"/> (x <xsl:value-of select="cantidad"/>)</td>
                        <td class="right">$<xsl:value-of select="format-number(importe, '0.00')"/></td>
                    </tr>
                </xsl:for-each>
                <tr class="total">
                    <td></td>
                    <td class="right">Subtotal: $<xsl:value-of select="format-number(totales/subtotal, '0.00')"/></td>
                </tr>
                 <tr class="total">
                    <td></td>
                    <td class="right">Impuestos: $<xsl:value-of select="format-number(totales/impuestos, '0.00')"/></td>
                </tr>
                 <tr class="total">
                    <td></td>
                    <td class="right"><strong>Total: $<xsl:value-of select="format-number(totales/total, '0.00')"/></strong></td>
                </tr>
            </table>
        </div>
    </xsl:template>

</xsl:stylesheet>
