import requests
from bs4 import BeautifulSoup
import pandas
import datetime
import time
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

words = ["火箭少女", "孟美岐", "吴宣仪", "杨超越", "段奥娟", "Yamy", "赖美云", "张紫宁", "紫宁", "Sunnee", "李紫婷",
         "杨芸晴", "傅菁", "徐梦洁", "肖战", "王一博", "XZ", "wyb", "吴博", "啵啵", "百香桶", "丁禹兮", "蔡徐坤",
         "新京报"]
for w in words:
    jieba.add_word(w)

# ptd = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%m-%d')
ptd = datetime.datetime.today().strftime('%m-%d')

allDiscussions = []
total_page = 50
for i in range(0, total_page):
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
    subSoup = soup.find('table', {"class": "olt"})
    subSoup = subSoup.find_all('tr', {"class": ""})

    add_count = 0
    for s in subSoup:
        threadTime = s.find("td", {"nowrap": "nowrap", "class": "time"}).contents[0]
        tdate_s = datetime.datetime.strptime(threadTime, "%m-%d %H:%M").strftime("%m-%d")
        if tdate_s == ptd:
            title = s.find('td', {"class": "title"})
            title = title.find("a", {"class": ""}).get("title")
            allDiscussions.append(title)
            add_count = add_count + 1
    print("finished reading {0} - {1}, added {2}".format(i + 1, total_page, add_count))
    time.sleep(1)

total_dis = " ".join(allDiscussions)
mytext = " ".join(jieba.cut(total_dis))
wordcloud = WordCloud(font_path="simsun.ttf", width=1500, height=700).generate(mytext)
fig = plt.figure(figsize=(15, 7), dpi=100)
fig.add_axes([0, 0, 1, 1])
plt.imshow(wordcloud, interpolation='nearest', aspect='auto')
plt.axis("off")
plt.savefig('c:/test/wordCloud.png', figsize=(15, 7), dpi=100)
plt.show()
