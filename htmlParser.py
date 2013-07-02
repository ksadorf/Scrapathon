#!/usr/bin/python2.7
# coding: utf-8
import requests
import re
from pyquery import PyQuery as pq


class Rapport:
    """Classe contenant toutes les infos d'un rapport"""

    def __init__(self,url):
        """Un unique parametre l'url du rapport"""
	resultat = requests.get(url)
	document = pq(resultat.text).make_links_absolute(url)        

	tmp=document("#document_informationsODS p").html()
	resReg2=re.match('D\xe9liberation',tmp)
	if not resReg2 :
		raise ValueError("Url moisie")
	
	resReg1=re.search('(?:Conseil )(\w+)(?:/ )(.*)(?:\[)(.+)(?:\])',tmp)
	self.type=resReg1.group(1)
	self.date=resReg1.group(2)
	self.id = resReg1.group(3).split(' / ')

	self.head = document("#document_informationsODS h1").html()
	self.rapporteur =re.search('(?:\. M\. )(.+)(?:, rapporteur)',self.head).group(1).split(' et ') 
	self.all= pq('<div class="Rapport"></div>')
	self.all.append(document("#document_informationsODS"))
	self.all.append(document("#document_contentODS"))



#url = u"http://www.paris.fr/accueil/Portal.lut?page=webappcontainer&site_id=20&webapp_url=aHR0cDovL2EwNi5hcHBzLnBhcmlzLmZyL2EwNi9qc3Avc2l0ZS9Qb3J0YWwuanNwP3BhZ2U9b2Rz%0ALXNvbHIuZGlzcGxheV9kb2N1bWVudCZpZF9kb2N1bWVudD05NjA3MyZpdGVtc19wZXJfcGFnZT0y%0AMCZzb3J0X25hbWU9JnNvcnRfb3JkZXI9JnRlcm1zPSZxdWVyeT0mZnE9c2VhbmNlX3N0cmluZyUz%0AQUpVSU4lMjAyMDEx"
#
#r=Rapport(url)
#print r.rapporteur
#print r.type
#print r.date
#print r.id


