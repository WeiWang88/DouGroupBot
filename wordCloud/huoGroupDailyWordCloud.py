import requests
from bs4 import BeautifulSoup
import datetime
import time
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import collections
import pandas

words = ["火箭少女", "孟美岐", "吴宣仪", "杨超越", "段奥娟", "yamy", "赖美云", "张紫宁", "紫宁", "Sunnee", "李紫婷",
         "杨芸晴", "傅菁", "徐梦洁", "肖战", "王一博", "XZ", "wyb", "吴博", "啵啵", "丁禹兮", "蔡徐坤",
         "新京报", "罗云熙", "周深", "华晨宇", "许魏洲", "陈情令", "光点", "227", "张含韵", "鞠婧祎", "金扫帚",
         "诛仙", "禁哥", "谷嘉诚", "硬糖少女", "龙丹妮", "杜华", "乐华", "吴博", "陈腾跃", "且听凤鸣", "黄景瑜"]
for w in words:
    jieba.add_word(w)
jieba.load_userdict("user.dict")

# ptd = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%m-%d')
ptd = datetime.datetime.today().strftime('%m-%d')

allDiscussions = []
total_page = 150
all_author = []
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
            author = s.find('td', {"class": ""})
            author = author.find("a", {"class": ""}).contents[0]
            all_author.append(author)
            allDiscussions.append(title)
            add_count = add_count + 1
            if add_count >= 25:
                break
    print("finished reading {0} - {1}, added {2}".format(i + 1, total_page, add_count))
    time.sleep(1)


author_ranking = collections.Counter(all_author)
output_author_ranking = author_ranking.most_common(20)
df = pandas.DataFrame(columns=["研究员", "发帖数"])
df_ind = 0
for s in output_author_ranking:
    df.loc[df_ind] = s
    df_ind = df_ind + 1
df.to_csv("c:/test/user.csv", encoding="UTF-32")

total_dis = " ".join(allDiscussions)
total_dis = total_dis.replace("今天", "")
total_dis = total_dis.replace("一个", "")
total_dis = total_dis.replace("真的", "")
total_dis = total_dis.replace("你们", "")
total_dis = total_dis.replace("大家", "")
total_dis = total_dis.replace("什么", "")
total_dis = total_dis.replace("这个", "")
total_dis = total_dis.replace("是不是", "")
total_dis = total_dis.replace("不是", "")
total_dis = total_dis.replace("觉得", "")
total_dis = total_dis.replace("怎么", "")
total_dis = total_dis.replace("一下", "")
total_dis = total_dis.replace("还是", "")
total_dis = total_dis.replace("看看", "")
total_dis = total_dis.replace("有没有", "")
total_dis = total_dis.replace("没有", "")
total_dis = total_dis.replace("不是", "")
total_dis = total_dis.replace("知道", "")
total_dis = total_dis.replace("有人", "")
total_dis = total_dis.replace("不会", "")
total_dis = total_dis.replace("不要", "")
total_dis = total_dis.replace("看到", "")
total_dis = total_dis.replace("现在", "")
total_dis = total_dis.replace("这么", "")
total_dis = total_dis.replace("那个", "")
total_dis = total_dis.replace("已经", "")
total_dis = total_dis.replace("所以", "")
total_dis = total_dis.replace("刚刚", "")
total_dis = total_dis.replace("关于", "")
total_dis = total_dis.replace("就是", "")
total_dis = total_dis.replace("发现", "")
total_dis = total_dis.replace("进来", "")
total_dis = total_dis.replace("这是", "")
total_dis = total_dis.replace("这样", "")


mytext = " ".join(jieba.cut(total_dis))
wordcloud = WordCloud(font_path="simsun.ttf", width=1500, height=700).generate(mytext)
fig = plt.figure(figsize=(15, 7), dpi=100)
fig.add_axes([0, 0, 1, 1])
plt.imshow(wordcloud, interpolation='nearest', aspect='auto')
plt.axis("off")
plt.savefig('c:/test/wordCloud.png', figsize=(15, 7), dpi=100)
plt.show()
