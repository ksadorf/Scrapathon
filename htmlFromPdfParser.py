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
		_regId='(\d{4} \w{1,4}\.? \w*\ ?( \w)?(\/\d{4} \w{1,4}\.? \w*)*)'
		__regId='(\d{4} \W{1,6}\.? \w*\ ? \w?(\/\d{4} \W{1,6}\.? \w*)*)'
		regId='(\d{4} [A-Z0-9_]{1,6}\.? [^\/|-|\<|\:]*([\/|-] ?\d{4} [A-Z0-9_]{1,6}\.? [^\/|-]*)*)'
		res=re.search(regType,inner)
		if res:
			self._type_=res.group(1)
			return
		res=re.search(regRap,inner)
		if res:
			tmp=re.search('et',res.group(1))
			if tmp:
				self._rapporteur_=res.group(1).split('et')
			else:
				self._rapporteur_=res.group(1)
			return
		
		res=re.search(regDate,inner)
		if res:
			
			tmp=re.search('(?:.*et )?(.*)',res.group(1))
			self._date_=tmp.group(1)
			return
		if re.search('\-{2,}',inner) :
			return

		res=re.search(regId,inner)
		if res :
			tmp=re.search('/',res.group(0))
			if tmp:
				self._id_=res.group(0).split('/')
			else:
				tmp=re.search('-',res.group(0))
				if tmp :
					self._id_=res.group(0).split('-')
				else:
					self._id_=res.group(0)
			return
		


	def __init__(self,id):
        	"""Un unique parametre le path du rapport"""
		self._type_=""
		self._rapporteur_=[]
		self._date_=''
		self._id_=[]
		self.content= ''
		self._empty_=False
		
		document = open('./scrapathon_2/'+str(id)+'.html', 'r').read()
		doc=pq(document)
		if not doc('span'):
			self._empty_=True
			return
			#Rien a parser
		bold= doc('span[style*="TimesNewRomanPS-BoldMT"]')
		if not bold:
			bold=doc('span[style*="Times-Bold"]')
		step1=re.sub('\</?(span|a|div|body|html|head|meta).*\>','',doc.html())
		step2 =''.join(re.sub('\-{2,}','--',step1).split('--')[-1])
		step3=re.sub("\s\s+",' ',step2)
		self.content=re.sub('((\\n)|(<br/?>))','',step3)

		for element in bold.items() :
			inner=element.html()
			#print "innner :"
			#print inner
			#print
			self._regexpCheck_(inner)
		#print
		#print "Sauvegardé :"
		#print self._type_
		#print self._rapporteur_
		#print self._date_
		#print self._id_
		#print self.content
		
		
	def isSufficient(self):
		if (self._rapporteur_!=[] or self._id_!=[]) :
			return True
		return False
		
			
			
			
for id in range(98301, 99404):
	r=Rapport(id)
	if not ( r.isSufficient()) and not (r._empty_==True) :
		print 'Warning ' + id
	else:
		if r._id_==[] and not (r._empty_==True):
			print id
		#print r._id_

r=Rapport(98303)
print r._id_


#rapporteur
#id
#date
#Municipale/general
