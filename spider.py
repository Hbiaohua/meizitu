import requests
from pyquery import PyQuery as pq
import re
import os
import time

#获得初始html
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36'}
def get_html(url):
    try:
        r = requests.get(url,headers=headers)
        if r.status_code==200:
            return r.text
        else:
            return None
    except:
        return  None

#解析html获得图片链接url(pic_url)
def parse_page(html):
    doc = pq(html)
    items = doc('#maincontent > div.inWrap > ul > li > div > h3 > a').items()
    for item in items:
        yield item.attr('href')

#获得末页，供循环用
def last_page(html):
    doc = pq(html)
    last_page = doc('ul > li:nth-child(18) > a').attr('href')
    num = re.findall(r'(\d+)',last_page)
    last_num = ''.join(num)
    return last_num

#解析图片页面，返回所有单个图片地址
def detail_page(html):
    doc = pq(html)
    pic_urls = doc('#picture > p > img').items()
    for pic_url in pic_urls:
        yield pic_url.attr('src')

#保存图片至本地
def save_pics(url):
    root = "E://meizitu//"
    path = root + url.replace('/','')[-15:]
    try:
        if not os.path.exists(root): #不存在则执行下个语句
            os.mkdir(root)           #创建目录
        if not os.path.exists(path):
            r = requests.get(url,headers=headers)
            with open(path,'wb') as f:
                f.write(r.content)
                f.close()
                print('图片保存成功')
        else:
            print('图片已保存')
    except:
        print('爬取错误')

def main():
    start_url = 'http://www.meizitu.com/a/more_1.html'
    html = get_html(start_url)
    last_num = last_page(html)
    for i in range(1, int(last_num)+1):
        url = 'http://www.meizitu.com/a/more_{}.html'.format(i)
        html = get_html(url)
        page_urls = parse_page(html)
        for page_url in page_urls:
            html = get_html(page_url)
            urls = detail_page(html)
            for url in urls:
                time.sleep(2)
                print(url)
                save_pics(url)

if __name__=='__main__':
    main()