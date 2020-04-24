from dbconnect import connection
import requests
from bs4 import BeautifulSoup
import warnings


def InsertSql(myDict,table):
    try:
        print('INSERINDO AGENDA....')
        c, conn = connection()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in myDict.keys())
            values = ', '.join("'" + str(x) + "'" for x in myDict.values())
            c.execute('SET @@auto_increment_increment=1;')
            conn.commit()
            sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table, columns, values)
            c.execute(sql)
            conn.commit()
        print(f'INSERIDO : { myDict} {{status :: OK}} ')
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))
def SelectSql(table, coluna,value):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM {table} WHERE {coluna}= '{value}'""")
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))

def UpdateQuerySql(mydict,table,item,modifica):
    print(' ATUALIZANDO DADOS .... ')
    c, conn = connection()
    for k in mydict:
        coluna = (k)
        value = (mydict[k])
        sql = (f"""UPDATE `{table}` SET `{coluna}` = '{value}' WHERE (`{item}` = '{modifica}');""")
        c.execute(sql)
        conn.commit()
        conn.close
    print(f'--->>> ATUALIZAÇÃO da TABELA :{table}  == > DATA {mydict}{{status :: OK}} .... ')



def delete_all_rows(table):
    try:
        print(f'DELETENDO ITENS DA TABELA {table}....')
        c, conn = connection()
        sql = "DELETE FROM %s ;" % (table)
        c.execute(sql)
        conn.commit()
        print('TODAS AS ROWS FORAM DELETADAS {{status :: OK}} ')
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))
def eventos():
    delete_all_rows('eventos')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    url = "https://mobile.facebook.com/pg/cervejariacriolina/events/"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    divs = soup.find_all('div', {'class', '_5zma'})

    for item in divs:
        # print(item)
        tabs = item.find_all('div', {'class', '_2x2s'})
        for i in tabs:
            # print(i)
            title = i.find('h3', {'class', '_592p _r-i'}).text
            dia = i.find('span', {'class', '_1e3a'}).text
            mes = i.find('span', {'class', '_1e39'}).text
            hora = i.find('span', {'class', '_592p'}).text.replace('UTC-03', '')


            myDict = {
                'EVENTO':title,
                'DIA': dia,
                'MES' :mes,
                'HORA':hora,
                'STATUS': 'OK'
            }
            # print(myDict)

            InsertSql(myDict,'eventos')



from selenium import webdriver
from bs4 import BeautifulSoup as bs
import json

def instagram_fotos():
    username = 'cervejariacriolina'
    browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    browser.get('https://www.instagram.com/' + username + '/?hl=en')
    # Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # links = []
    source = browser.page_source
    data = bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)

    for link in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        # print(link['node']['display_url'])
        myDict = {'LINK':link['node']['display_url'],
                  'STATUS':'OK'}
        check = SelectSql('instagram','LINK', link['node']['display_url'])
        if check == False:

            InsertSql(myDict,'instagram')

