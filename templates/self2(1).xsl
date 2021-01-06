<?xml version="1.0"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">


-<xsl:template match="/">


-<html>


-<head>

<title>XML XSL Example</title>

<style type="text/css">body {margin:10px;background-color:lightblue;font-family:verdana,helvetica,sans-serif;}.tutorial-name {display:block;font-weight:bold;background-color:cyan;text-align:center;}.tutorial-url {display:block;color:#636363;font-size:small;font-style:italic;text-align:center;} </style>

</head>


-<body>

<h2>List of Student With there domain name</h2>

<xsl:apply-templates/>

</body>

</html>

</xsl:template>


-<xsl:template match="tutorial">


-<span class="tutorial-name">

<xsl:value-of select="name"/>

</span>


-<span class="tutorial-url">

<xsl:value-of select="url"/>

</span>

</xsl:template>

</xsl:stylesheet>
