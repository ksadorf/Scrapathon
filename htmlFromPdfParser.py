#!/usr/bin/python2.7
# coding: utf-8
import requests
import re
from pyquery import PyQuery as pq


class Rapport:
	"""Classe contenant toutes les infos d'un rapport"""
	
	"""Regexp pour trouver un le type d'un conseil"""
	
	def _regexpCheck_(self, inner):
		inner=re.sub("\s\s+",' ',inner) #remove multiple space
		regType='(?:Conseil )(Municipal|Général)'
		regRap='(.*)(?:, rapporteur)'
		regDate='(?:S.ance )(?:des )?(.*\d{4})'
		idPos='\d{4} \w{3,4}\ *\w*'
		regId='(\d{4} \w{3,4} \w*\ ?(\/\d{4} \w{3,4} \w*)*)'
		res=re.search(regType,inner)
		if res:
			self._type_=res.group(1)
			return
		res=re.search(regRap,inner)
		if res:
			self._rapporteur_=res.group(1)
			return
		
		res=re.search(regDate,inner)
		if res:
			self._date_=res.group(1)
			return
		if re.search('\-{2,}',inner) :
			return

		res=re.search(regId,inner)
		if res :
			tmp=res.group(1)
			print "id"+tmp
			self._id_=tmp.split('/')
			return
		


	def __init__(self,id):
        	"""Un unique parametre le path du rapport"""

		
		document = open('./scrapathon_2/'+str(id)+'.html', 'r').read()
		doc=pq(document)
		bold= doc('span[style*="TimesNewRomanPS-BoldMT"]')
		if bold:
			print "trouve"
		else:
			bold=doc('span[style*="Times-Bold"]')
		step1=re.sub('\</?(span|a|div|body|html|head|meta).*\>','',doc.html())
		print "1"
		print step1
		step2 =''.join(re.sub('\-{2,}','--',step1).split('--')[-1])
		print "2"
		print step2
		step3=re.sub("\s\s+",' ',step2)
		print "3"
		print step3
		self.content=re.sub('((\\n)|(<br/?>))','',step3)

		for element in bold.items() :
			inner=element.html()
			#print "innner :"
			#print inner
			#print
			self._regexpCheck_(inner)
		print
		print "Sauvegardé :"
		#print self._type_
		#print self._rapporteur_
		#print self._date_
		#print self._id_
		print self.content
		
			
			
			
#for id in range(98301, 151480):
#	path="./scrapathon_2/"+str(id)+".html"
#	r=Rapport(path)

r=Rapport(98303)


#rapporteur
#id
#date
#Municipale/general
