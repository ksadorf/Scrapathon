#!/usr/bin/python2.7
# coding: utf-8
import requests
import re
from pyquery import PyQuery as pq
import pickle

class Rapport:
	"""Classe contenant toutes les infos d'un rapport"""
	
	"""Regexp pour trouver un le type d'un conseil"""
	
	def _regexpCheck_(self, inner):
		inner=re.sub("\s\s+",' ',inner) #remove multiple space
		regType='(?: )?(Municipal|G.n.ral)(?: )?'
		regRap='(.*)(?:, rapporteur)'
		regDate='(?:S.ance )(?:des|du )?(.*\d{4})'
		_regId='(\d{4} \w{1,4}\.? \w*\ ?( \w)?(\/\d{4} \w{1,4}\.? \w*)*)'
		__regId='(\d{4} \W{1,6}\.? \w*\ ? \w?(\/\d{4} \W{1,6}\.? \w*)*)'
		regId='(\d{4} [A-Z0-9_]{1,10}\.? [^\/|-|\<|\:]*([\/|-] ?\d{4} [A-Z0-9_]{1,6}\.? [^\/|-]*)*)'
		res=re.search(regType,inner)
		if res:
			self._type_=res.group(1)
			return
		res=re.search(regRap,inner)
		if res:
			tmp=re.search('et',res.group(1))
			if tmp:
				self._rapporteur_=re.split('et|,',res.group(1))
				i=len(self._rapporteur_)
				while i!=0:

					elem=self._rapporteur_[i-1]
					if (len(elem)<3 ):self._rapporteur_.remove(self._rapporteur_[i-1])
					i=i-1
			else:
				self._rapporteur_=[res.group(1)]
			return
		
		res=re.search(regDate,inner)
		if res:
			self._date_=res.group(1)
			tmp=re.search('(?: et )?(.*)',res.group(1))
			if tmp :
				self._date_=tmp.group(0).split(' et ')[-1]				
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
					self._id_=[res.group(0)]
			i=len(self._id_)
			while i!=0:

				elem=self._id_[i-1]
				if (len(elem)<3 or re.search('[^A-Z0-9_ ]',elem) ):self._id_.remove(self._id_[i-1])
				i=i-1
			
			return
		


	def __init__(self,id):
        	"""Un unique parametre le path du rapport"""
        	self._pdfId_=id
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
		
			
			
tab=[]		
for id in range(98301, 111479):
	r=Rapport(id)
	if (r._empty_==True) :
		print 'Warning ' , id
	else:
		print id,'/111479'
		tab.append(r)
output=open('DelibConseil', 'w')
pickle.dump(tab,output)
print "FIN"

#usage to re-load picle object :
# input = open('DelibConseil', 'r')
# delib = pickle.load(input)

#rapporteur
#id
#date
#Municipale/general


rapporteurs=dict()
for row in delib:
	for rap in row._rapporteur_:
		rap_new = str(rap.encode('utf-8')).replace("<br/>","").replace("Mmes","").replace("M.","").replace("Mme","").replace("Madame","").replace("Monsieur","").strip()
		if rap_new not in rapporteurs:
		    rapporteurs[rap_new] = 0
		rapporteurs[rap_new]= rapporteurs[rap_new]+1

sorted(rapporteurs.items(), key=lambda x: x[1])