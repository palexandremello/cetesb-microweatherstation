#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt

url = 'http://qualar.cetesb.sp.gov.br/qualar/home.do'
url_post_pgin = 'http://qualar.cetesb.sp.gov.br/qualar/autenticador'
url_post_pgin2 = 'http://qualar.cetesb.sp.gov.br/qualar/exportaDados.do'
payload = {"cetesb_login": "palexandremello@gmail.com",
           "cetesb_password": "147258loki", "enviar": "OK"}

postHeaders = {
    'Accept-Language': 'en-US,en;q=0.8',
    'Origin': 'http://www.website.com',
    'Referer': 'http://www.website.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36'
}


session = requests.Session()

response = session.post(url, data=payload, headers=postHeaders)

response = session.post(url_post_pgin, data=payload, headers=postHeaders)


data = {'method': 'pesquisar', 'irede': 'A',
        'dataInicialStr': '27/08/2018', 'dataFinalStr': '27/08/2018',
        'cDadosInvalidos:': 'on', 'iTipoDado': 'P',
        'estacaoVO.nestcaMonto': '288', 'parametroVO.nparmt': '28'}

response = session.post(url_post_pgin2, data=data, headers=postHeaders)

doc = lh.fromstring(response.content)

tr_elements = doc.xpath('//tr')[5:]

col = []
i = 0

# For each row, store each first element (header) and an empty list
elements = ['', 'Tipo de Rede', 'Tipo de Monitoramento', 'Tipo',
            'Data', 'Hora', 'Código Estação',
            'Nome Estação', 'Nome Parâmetro', 'Unidade de Medida',
            'Média Horária', 'Média Móvel', 'Válido',
            'Dt. Amostragem', 'Dt. Instalação', 'Dt. Retirada',
            'Concentração', 'Taxa', '']
for t in elements:
    i += 1
    # name=t.text_content().strip()
    #print ('%d:"%s"'%(i,name))
    col.append((t, []))


for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]
    # If row is not of size 10, the //tr data is not from our table
    if len(T) != 19:
        break

    # i is the index of our column
    i = 0

    # Iterate through each element of the row
    for t in T.iterchildren():
        data = t.text_content().strip().replace(',', '.')
        # Check if row is empty
        if i > 0:
            # Convert any numerical value to integers
            try:
                data = int(data)
            except:
                pass

        # Append the data to the empty list of the i'th column
        col[i][1].append(data)
        # Increment i for the next column
        i += 1


Dict = {title: column for (title, column) in col}

df = pd.DataFrame(Dict)

try:
    df['Média Horária'] = df['Média Horária'].replace(
        {',': '.'}, regex=True).astype('float64')
except:
    pass

print(df['Média Horária'].values)
plt.figure()
df['Média Horária'].plot()
plt.show()



