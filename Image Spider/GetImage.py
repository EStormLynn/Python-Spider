#coding: utf-8
import os
import re
import urllib
import urllib2
import itertools  #迭代器
from string import maketrans

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

intab="wkv1ju2it3hs4g5rq6fp7eo8dn9cm0bla"
outtab="abcdefghijklmnopqrstuvw1234567890"
trantab = maketrans(intab, outtab)

char_table = {ord(key): ord(value) for key, value in char_table.items()}
def deCode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    d=url.translate(trantab)
    return d

def getMoreURL(word):
    word = urllib.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}" \
          r"&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=30"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=30))
    #itertools.count 0开始，步长30，迭代
    return urls

def getHtml(url):
    page=urllib.urlopen(url)
    html=page.read()
    return html

#解析图片url解码
def getImg(html):
    reg=r'"objURL":"(.*?)"'   #正则
    # 括号表示分组，将括号的内容捕获到分组当中
    #  这个括号也就可以匹配网页中图片的url了
    imgre=re.compile(reg)
    imageList=re.findall(imgre, html)
    imgUrls=[]

    for image in imageList:
        imgUrls.append(deCode(image))

    l=len(imgUrls)
    print l
    return imgUrls

def downLoad(urls,path):
    global index
    for url in urls:
        print("Downloading:", url)
        res = urllib2.Request(url)
        try:
            response = urllib2.urlopen(res ,data=None, timeout=5)  #超时处理
        except urllib2.URLError, e:
            if hasattr(e,'code'):
                error_status = e.code
                print(error_status, "未下载成功：", url)
                continue
            elif hasattr(e,'reason'):
                print( "time out", url)
                continue

            continue

        filename = os.path.join(path, str(index) + ".jpg")
        urllib.urlretrieve(url,filename)        #直接将远程数据下载到本地。
        index += 1
        # urllib.urlretrieve(url[, filename[, reporthook[, data]]])
        # 参数说明：
        # url：外部或者本地url
        # filename：指定了保存到本地的路径（如果未指定该参数，urllib会生成一个临时文件来保存数据）；
        # reporthook：是一个回调函数，当连接上服务器、以及相应的数据块传输完毕的时候会触发该回调。我们可以利用这个回调函数来显示当前的下载进度。
        # data：指post到服务器的数据。该方法返回一个包含两个元素的元组(filename, headers)，filename表示保存到本地的路径，header表示服务器的响应头。
        if index-1==1000:
            break

if __name__ == '__main__':
    keyWord="新垣结衣"
    index = 1
    Savepath = "D:\TestDownload"
    urls=getMoreURL(keyWord)

    for url in urls:
        downLoad(getImg(getHtml(url)),Savepath)
        if index-1==1000:
            break