#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-10-14 21:05:28
# Project: meizitu

from pyspider.libs.base_handler import *
import time
import requests
import os

ROOT = "E://meizitu_2//"  # 存放目录
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36'}

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.root = ROOT
        self.headers = HEADERS

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.meizitu.com/a/more_1.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div.con > h3 > a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        items = response.doc('#picture > p > img').items()
        for item in items:
            self.crawl(item.attr.src, callback=self.save_picture)

    def on_result(self, response):
        if response:
            time.sleep(2)
            self.save_picture(response)

    def save_picture(self, response):
        url = response.url
        content = response.content
        root = "E://meizitu//"
        path = root + url.replace('/', '')[-15:]
        print(path)
        try:
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    r = requests.get(url)
                    f.write(content)
                    f.close()
                    print('图片保存成功')
            else:
                print('图片已保存')
        except:
            print('爬取错误')