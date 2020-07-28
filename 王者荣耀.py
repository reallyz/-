import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from tqdm import tqdm

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
base_url='https://pvp.qq.com/web201605/'
with open(r'd:\hobbies\爬虫\herolist.txt','r',encoding='utf-8') as f:
    te=f.readlines()
urlist=list(map(lambda x:x.strip(),te))

def get_info(url):
    ls=[]
    html=requests.get(url=base_url+url,headers=headers)
    soup = BeautifulSoup(html.content, 'lxml')
    heroname=soup.find('h2').text
    ls.append(heroname)
    lshero = soup.find_all('div', class_='hero-list-desc')
    for item in lshero:
        for p in item.find_all('p'):
            out=p.text
            if '：' in out:
                pos=out.find('：')
                out=out[:pos]
            ls.append(out)
    lsskill = soup.find_all('div', class_='show-list')
    for skill in lsskill:
        ls.append(skill.find('p', class_='skill-desc').text)
    return ls

heros=[]
desc=['英雄名字','搭配英雄','压制英雄','受压制英雄','被动','技能1','技能2','技能3','技能4']
heros.append(desc)
bar=tqdm(urlist)
for item in bar:
    bar.set_description('Processing %s'%item)
    time.sleep(1)
    hero=get_info(item)
    heros.append(hero)
df=pd.DataFrame(heros)
df.to_excel('herosfeature.xls')
