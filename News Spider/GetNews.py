#coding=utf-8
import re  # 正则表达式
import bs4  # Beautiful Soup 4 解析模块
import urllib2  # 网络访问模块
import News
import codecs  #解决编码问题的关键 ，使用codecs.open打开文件
import sys   #1

reload(sys)                         # 2
sys.setdefaultencoding('utf-8')     # 3

# 从首页获取所有链接
def GetAllUrl(home):
    html = urllib2.urlopen(home).read().decode('utf8')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    pattern = 'http://\w+\.baijia\.baidu\.com/article/\w+'
    links = soup.find_all('a', href=re.compile(pattern))
    for link in links:
        url_set.add(link['href'])

def GetNews(url):
    global NewsCount,MaxNewsCount  #全局记录新闻数量
    while len(url_set) != 0:
        try:
            # 获取链接
            url = url_set.pop()
            url_old.add(url)

            # 获取代码
            html = urllib2.urlopen(url).read().decode('utf8')

            # 解析
            soup = bs4.BeautifulSoup(html, 'html.parser')
            pattern = 'http://\w+\.baijia\.baidu\.com/article/\w+'  # 链接匹配规则
            links = soup.find_all('a', href=re.compile(pattern))

            # 获取URL
            for link in links:
                if link['href'] not in url_old:
                    url_set.add(link['href'])

                    # 获取信息
                    article = News.News()
                    article.url = url  # URL信息
                    page = soup.find('div', {'id': 'page'})
                    article.title = page.find('h1').get_text()  # 标题信息
                    info = page.find('div', {'class': 'article-info'})
                    article.author = info.find('a', {'class': 'name'}).get_text()  # 作者信息
                    article.date = info.find('span', {'class': 'time'}).get_text()  # 日期信息
                    article.about = page.find('blockquote').get_text()
                    pnode = page.find('div', {'class': 'article-detail'}).find_all('p')
                    article.content = ''
                    for node in pnode:  # 获取文章段落
                        article.content += node.get_text() + '\n'  # 追加段落信息

                    SaveNews(article)

                    print NewsCount
                    break
        except Exception as e:
            print(e)
            continue
        else:
            print(article.title)
            NewsCount+=1
        finally:
            # 判断数据是否收集完成
            if NewsCount == MaxNewsCount:
                break

def SaveNews(Object):
    file.write("【"+Object.title+"】"+"\t")
    file.write(Object.author+"\t"+Object.date+"\n")
    file.write(Object.content+"\n"+"\n")

url_set = set()  # url集合
url_old = set()  # 爬过的url集合

NewsCount = 0
MaxNewsCount=3

home = 'http://baijia.baidu.com/'  # 起始位置

GetAllUrl(home)

file=codecs.open("D:\\test.txt","a+") #文件操作

for url in url_set:
    GetNews(url)
    # 判断数据是否收集完成
    if NewsCount == MaxNewsCount:
        break

file.close()