import requests
from bs4 import BeautifulSoup
import pandas
import datetime
import time
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

words = ["火箭少女", "孟美岐", "吴宣仪", "杨超越", "段奥娟", "Yamy", "赖美云", "张紫宁", "紫宁", "Sunnee", "李紫婷",
         "傅菁", "徐梦洁", "肖战", "王一博"]
for w in words:
    jieba.add_word(w)


# ptd = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%m-%d')
ptd = datetime.datetime.today().strftime('%m-%d')

allDiscussions = []
for i in range(0, 60):
    s = requests.session()
    s.headers.update({
        'Host': 'www.douban.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    startCount = i * 25
    resp = s.get('https://www.douban.com/group/ihuo/discussion?start={0}'.format(startCount))
    soup = BeautifulSoup(resp.text, 'html.parser')
    subSoup = soup.find('table', {"class":"olt"})
    subSoup = subSoup.find_all('tr', {"class":""})

    for s in subSoup:
        threadTime = s.find("td", {"nowrap":"nowrap", "class":"time"}).contents[0]
        tdate_s = datetime.datetime.strptime(threadTime, "%m-%d %H:%M").strftime("%m-%d")
        if tdate_s == ptd:
            title = s.find('td', {"class":"title"})
            title = title.find("a", {"class":""}).get("title")
            allDiscussions.append(title)
    print("finished reading {0} - {1}".format(i+1, 60))
    time.sleep(1)

total_dis = " ".join(allDiscussions)
mytext = " ".join(jieba.cut(total_dis))
wordcloud = WordCloud(font_path="simsun.ttf").generate(mytext)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
