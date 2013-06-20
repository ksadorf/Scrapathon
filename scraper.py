#!/usr/bin/python2.7
# coding: utf-8
import requests
from urllib2 import Request, urlopen
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO


111480
for id in range(98301, 111480):
	url = u"http://a06.apps.paris.fr/a06/jsp/site/plugins/solr/modules/ods/DoDownload.jsp?id_document=1"+str(id)
	writer = PdfFileWriter()
	try:
		remoteFile = urlopen(Request(url)).read()
		memoryFile = StringIO(remoteFile)
		pdfFile = PdfFileReader(memoryFile)
		for pageNum in xrange(pdfFile.getNumPages()):
		    currentPage = pdfFile.getPage(pageNum)
		    #currentPage.mergePage(watermark.getPage(0))
		    writer.addPage(currentPage)

		outputStream = open(str(id)+".pdf","wb")
		writer.write(outputStream)
		outputStream.close()
	except:
		print str(id)+" not found"
		pass
	finally:
		print str(id)+" Done"
