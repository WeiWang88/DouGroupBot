import requests
from bs4 import BeautifulSoup
import pandas


s = requests.session()
s.headers.update({
    'Host': 'www.douban.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
})
resp = s.get('https://www.douban.com/group/topic/181085482/')
soup = BeautifulSoup(resp.text, 'html.parser')

subsoup = soup.find('ul', {'class':"topic-reply", 'id':"comments"})
subsoups = subsoup.find_all('li', {'class':"clearfix comment-item reply-item"})

df = pandas.DataFrame(columns=['href', 'username', 'comment'])
rowCount = 0
for s in subsoups:
    user = s.find('a', {'class': ''})
    href = user.get('href')
    username = user.find('img').get('alt')
    comment = s.find('p', {"class": "reply-content"}).contents[0]
    df.loc[rowCount] = [href, username, comment]
    rowCount = rowCount + 1

for page in [100, 200, 300, 400, 500, 600, 700, 800]:
    s = requests.session()
    s.headers.update({
        'Host': 'www.douban.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    resp = s.get('https://www.douban.com/group/topic/181085482/?start={0}'.format(page))
    soup = BeautifulSoup(resp.text, 'html.parser')
    subsoup = soup.find('ul', {'class':"topic-reply", 'id':"comments"})
    subsoups = subsoup.find_all('li', {'class':"clearfix comment-item reply-item"})
    for s in subsoups:
        user = s.find('a', {'class': ''})
        href = user.get('href')
        username = user.find('img').get('alt')
        comment = s.find('p', {"class": "reply-content"}).contents[0]
        df.loc[rowCount] = [href, username, comment]
        rowCount = rowCount + 1

# df[df['comment'] == 'dd'].shape
df = df[df['comment'] != 'dd']
df = df[df['comment'] != 'up']
df = df[df['comment'] != '顶']
df = df[df['comment'] != '顶顶']
df.to_csv("C:/test/all_comments.CSV", encoding='utf-8-sig')