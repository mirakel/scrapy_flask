from bs4 import BeautifulSoup
import requests
import json

def info_episodes():
    url = 'https://es.wikipedia.org/wiki/Anexo:Episodios_de_Juego_de_tronos'
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'lxml')
    tables = soup.findAll('table', {'class','wikitable'})
    episodes = []

    for i in range(1,len(tables)):
        ep = 1
        rows = tables[i].findAll('tr')
        for j in range(1, len(rows)):
            columns = rows[j].findAll('td')
            if(len(columns) > 1):
                info = columns[2].text.split("\n")
                title = info[1].replace(u'\u200b',' ').split('[')[0]
                original = info[0].replace(u'\xa0', ' ')
                elements = {'title': title, 'title_original': original, 'n_episode':ep}
                ep = ep + 1
            else:
                elements['synopsis'] = columns[0].text
            elements['seasonId'] = i

            if(len(elements) == 4):
                episodes.append(elements)

    return json.dumps(episodes)

def info_videos():
    url = 'https://api.fruithosted.net/file/listfolder?login=t6Hg4K4QiW&key=y23yt3KF&folder=142793'
    response = requests.get(url)
    return json.loads(response.text)

def get_splash(file):
    url = 'https://api.fruithosted.net/file/getsplash?login=t6Hg4K4QiW&key=y23yt3KF&file=' + file
    response = requests.get(url)
    return json.loads(response.text)

def info_seasons():
    url = 'https://es.wikipedia.org/wiki/Anexo:Episodios_de_Juego_de_tronos'
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'lxml')
    tag = soup.find('li',{'class','tocsection-1'})
    lists = tag.find('ul').findAll('span', {'class','toctext'})
    seasons = []

    for title in lists:
        seasons.append({'title': title.text[:-7]})

    return json.dumps(seasons)
