from urllib2 import Request, urlopen
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO
from htmlParser import *
import sys

#548 10 entre juillet 2011 et juin 2013


# on en prend 13 179
#98301
for id in range(98301, 151480):
	url = u"http://a06.apps.paris.fr/a06/jsp/site/plugins/solr/modules/ods/DoDownload.jsp?id_document="+str(id)
	writer = PdfFileWriter()
	try:
		remoteFile = urlopen(Request(url)).read()
		if( "%PDF" in remoteFile):
			memoryFile = StringIO(remoteFile)
			pdfFile = PdfFileReader(memoryFile)
			for pageNum in xrange(pdfFile.getNumPages()):
			    currentPage = pdfFile.getPage(pageNum)
			    #currentPage.mergePage(watermark.getPage(0))
			    writer.addPage(currentPage)

			outputStream = open("scrapathon/"+str(id)+".pdf","wb")
			writer.write(remoteFile)
			outputStream.close()
		else:
			outputStream = open("htmlBase/"+str(id)+".html","wb")
			outputStream.write(remoteFile)
			outputStream.close()
	except:
		print "Unexpected error:", sys.exc_info()[0]
		print "Unexpected error:", sys.exc_info()[1]
		print str(id)+" not found"
		pass
	else:
		print str(id)+" Done"
