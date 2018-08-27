#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

class cetesb(object):
	"""docstring for cetesb"""
	def __init__(self):
		self.login = login
		self.senha = senha
		self.dataInicial = dataInicial
		self.dataFinal   = dataFinal
		self.estation    = estation
		self.parameter   = parameter
		self.exportcsv = exportcsv
		self.exportingToCsv = exportingToCsv

	def getData(dataInicial,dataFinal,estation,parameter,login='palexandremello@gmail.com', senha='xtQebUmw',exportcsv=False):
		import lxml.html as lh
		import requests
		cetesbHomepage = 'http://qualar.cetesb.sp.gov.br/qualar/home.do'
		cetesbAutent = 'http://qualar.cetesb.sp.gov.br/qualar/autenticador'
		usernameCredentials = {"cetesb_login":login,"cetesb_password":senha, "enviar": "OK"}
		postHeaders = {'Accept-Language': 'en-US,en;q=0.8','Origin': 'http://www.website.com', 'Referer': 'http://www.website.com/','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36'}
		session = requests.Session() ; response = session.post(cetesbHomepage, data=usernameCredentials, headers=postHeaders)
		response = session.post(cetesbHomepage, data=usernameCredentials, headers=postHeaders)
		response = session.post(cetesbAutent, data=usernameCredentials, headers=postHeaders)
		dataPage = 'http://qualar.cetesb.sp.gov.br/qualar/exportaDados.do'
		headerData = {'method': 'pesquisar', 'irede': 'A','dataInicialStr': dataInicial, 'dataFinalStr': dataFinal,'cDadosInvalidos:': 'on', 'iTipoDado': 'P','estacaoVO.nestcaMonto': estation, 'parametroVO.nparmt': parameter}
		response = session.post(dataPage, data=headerData, headers=postHeaders)

		data = cetesb.__unpackHTMLToData(lh.fromstring(response.content))
		return cetesb.__exportCSV(exportcsv,cetesb.__ToDict(data))

	def __unpackHTMLToData(content):
		import requests
		import lxml.html as lh
		tr_elements = content.xpath('//tr')[5:]
		col = []
		i = 0
		# For each row, store each first element (header) and an empty list
		elements = ['Retirar','TipoDeRede', 'TipoDeMonitoramento', 'Tipo',
		'Data', 'Hora', 'CódigoEstação',
		'NomeEstação', 'NomeParâmetro','UnidadeDeMedida',
		'MédiaHorária', 'MédiaMóvel','Válido',
		'Dt.Amostragem', 'Dt.Instalação','Dt.Retirada', 
		'Concentração', 'Taxa','Retirar2']
		
		for t in range(0,len(elements)):
			col.append((elements[t], []))
			i += 1
		
		for j in range(0, len(tr_elements)):
		# T is our j'th row
			T = tr_elements[j]
			if len(T) != 19:
				break
			i = 0
			for t in T.iterchildren():			    
			    data = t.text_content().strip()#.replace(',', '.')# Check if row is empty
			    if i > 0:
			    	try:
			    		data = int(data)
			    	except:
			    		pass
			    
			    col[i][1].append(data)
			    i += 1
		return col

	def __ToDict(data):
		import pandas
		Dict = {title: column for (title, column) in data}
		df = pd.DataFrame(Dict)
		try:
			df['MédiaHorária'] = df['MédiaHorária'].replace({',': '.'}, regex=True).astype('float64')
		except:
			pass
		return df

	def __exportCSV(exportingToCsv,df):
		import pandas as pd
		if exportingToCsv is True:
				varname = list(df.head(0))[8]
				datetime = df[list(df.head(0))[4]][0].replace('/','')
				codEst = df[list(df.head(0))[6]][0]
				parameterName = df[varname][0].split(' ')[0]
				df = df.drop(['Retirar','Retirar2'],axis=1)
				df.to_csv("Cod{0}_{1}_{2}.csv".format(codEst,parameterName,datetime), sep=',',encoding='utf-8',index=False)
				return df
		else:
			return df 
		  

vars = ['56','29']

import pandas as pd

for x in vars:
	df = cetesb.getData('27/08/2018','27/08/2018','288',x,exportcsv=True)
	df['MédiaHorária'].plot()
	plt.show()