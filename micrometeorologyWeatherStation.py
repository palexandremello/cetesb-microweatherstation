#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import csv 

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
		'Data', 'Hora', 'CodigoEstacao',
		'NomeEstacao', 'NomeParametro','UnidadeDeMedida',
		'MediaHoraria', 'MediaMovel','Valido',
		'Dt.Amostragem', 'Dt.Instalacao','Dt.Retirada', 
		'Concentracao', 'Taxa','Retirar2']
		
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
		import pandas as pd
		Dict = {title: column for (title, column) in data}
		df = pd.DataFrame(Dict)
		try:
			df['MediaHoraria'] = df['MediaHoraria'].replace({',': '.'}, regex=True).astype('float64')
		except:
			pass
		return df

	def __exportCSV(exportingToCsv,df):
		if exportingToCsv is True:
				df, varname, datetime, codEst, parameterName = cetesb.__getColumnsName(df)
				df.to_csv("Cod{0}_{1}_{2}.csv".format(codEst,parameterName,datetime), sep=',',encoding='utf-8',index=False)
				return df
		else:
			return df

	def CsvToJson(df, format='pretty'):
		import csv
		import pandas as pd
		df, varname, datetime, codEst, parameterName = cetesb.__getColumnsName(df)
		file="Cod{0}_{1}_{2}.csv".format(codEst,parameterName,datetime)
		jsonFile="Cod{0}_{1}_{2}.json".format(codEst,parameterName,datetime)
		csv_rows = []
		with open(file) as csvfile:
			reader = csv.DictReader(csvfile)
			title = reader.fieldnames
			for row in reader:
				csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])

			cetesb.__write_json(csv_rows, jsonFile, format)

	def __write_json(data, jsonFile, format='pretty'):
		import json
		with open(jsonFile, "w") as f:
			if format == "pretty":
				f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '),ensure_ascii=False))
			else:
				f.write(json.dumps(data))
	def __getColumnsName(df):
		import pandas as pd 
		for colName in df:
			if colName is 'Retirar':
				varname = list(df.head(0))[8]
				datetime = df[list(df.head(0))[4]][0].replace('/','')
				codEst = df[list(df.head(0))[6]][0]
				parameterName = df[varname][0].split(' ')[0]
				df = df.drop(['Retirar','Retirar2'],axis=1)
			elif colName is 'Retirar2':
				pass
			else:
				varname = list(df.head(0))[7]
				datetime = df[list(df.head(0))[3]][0].replace('/','')
				codEst = df[list(df.head(0))[5]][0]
				parameterName = df[varname][0].split(' ')[0]
		return df, varname, datetime, codEst, parameterName

import pandas as pdf

vars = ['56','29','63']

df = cetesb.getData('28/08/2018','28/08/2018','288',vars[2],exportcsv=True)
cetesb.CsvToJson(df)
df['MediaHorária'] = df['MediaHoraria'] * 0.29
df['MediaHoraria'].plot()
#plt.show()

				
#			else:
#				varname = list(df.head(0))[7]
#				datetime = df[list(df.head(0))[3]][0].replace('/','')
#				codEst = df[list(df.head(0))[5]][0]
#			    return df, varname, datetime, codEst, parameterName





#Convert csv data into json and write it



#print(cetesb.CsvToJson('Cod288_O3_28082018.csv','Cod288_O3_28082018.json'))