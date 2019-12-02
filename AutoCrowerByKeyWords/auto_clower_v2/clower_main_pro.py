#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
from utils import save_supplement_data
from download_file import download_file_use_middle_website
from text_analysis import text_content_analysis
import time
import random

def download_gaokaowang_page(search_key, base_url):
    print('开始下载文件 download start...')
    headers = {
        'user-agent': 'Mozilla/5.0'
    }
    url = base_url + search_key
    response = requests.get(url, headers=headers)
    # 1 get web page data
    # print(response.content) # print(response.text)
    web_page = response.content
    # 2 phrase web page data
    soup = BeautifulSoup(web_page, 'html.parser')  # 使用python默认的解析器
    # print(soup)
    next_page = soup.find_all('div', class_="page-b")
    # 存储该关键字搜索出现的搜索页码信息
    page_num_list = ['1']
    for np in next_page:
        for hr in np.find_all('a'):
            if hr.get_text().isdigit():
                page_num_list.append(hr.get_text())
    # print(page_num_list)
    if len(page_num_list) == 1:
        print('current search web_page has no next page')
        download_page(soup, search_key)
    else:
        # 爬每一页的资源
        for page_idx in page_num_list:
            curr_page = 'http://tiku.gaokao.com/search/type0/' + search_key + '/pg' + page_idx + '0'
            # print(curr_page)
            download_next_page(curr_page, search_key)
            time.sleep(1 + random.random() * 1 if (random.random() > 0.5) else -1)
        print('该关键词', search_key, ' 的相关资源已经获取完成,程序结束！！！')
    return


def download_next_page(url, search_key):
    response = requests.get(url)
    web_page = response.content
    # 2 phrase web page data
    soup = BeautifulSoup(web_page, 'html.parser')  # 使用python默认的解析器
    download_page(soup, search_key)


def download_page(soup, search_key):
    is_have_search_result = False
    res = soup.find_all('article', class_="result-item")
    if len(res) >0:
        is_have_search_result = True
    if is_have_search_result:
        curr_titles = []
        curr_middle_websites = []
        curr_introduction_contents = []
        # 3 get title & middle_website & introduction
        titles = soup.find_all('a', class_="c-l2")  # download_url = soup.find_all('a')
        for title in titles:
            curr_titles.append(title.get_text())
            curr_middle_websites.append(title.get('href'))
        introduction_contents = soup.find_all('p', class_="c-b6 ti2")
        for idc in introduction_contents:
            curr_introduction_contents.append(idc.get_text())
        # print(curr_titles)
        # print(curr_middle_websites)
        # print(curr_introduction_contents)
        # 保存爬取的信息
        # save_supplement_data(search_key, curr_titles, curr_middle_websites, curr_introduction_contents)
        # 下载文件
        download_file_use_middle_website(search_key, curr_titles, curr_middle_websites)
        print('文件下载成功...')
        print('开始文件分析...')
        text_content_analysis(search_key)
    else:
        print('没有找到该关键字', search_key, '相关的资源，程序结束。')
        return


def download_21shiji_page():
    # todo download 21shiji wang
    # 1. 创建session对象，可以保存Cookie值
    ssion = requests.session()
    # 2. 处理 headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    # 3. 需要登录的用户名和密码
    data = {"email": "mr_mao_hacker@163.com", "password": "alarmchime"}
    # 4. 发送附带用户名和密码的请求，并获取登录后的Cookie值，保存在ssion里
    ssion.post("http://www.renren.com/PLogin.do", data=data)
    # 5. ssion包含用户登录后的Cookie值，可以直接访问那些登录后才可以访问的页面
    response = ssion.get("http://www.renren.com/410043129/profile")
    # 6. 打印响应内容
    print(response.text)


def main():
    # input
    # key_words = ['光合作用', '圆锥曲线方程', '作用力']
    # key_words = ['光合作用']
    key_words = ['什么m']
    website_url_dict = {'gaokaowang':'http://tiku.gaokao.com/search/type0/',
                        '21shiji':'https://www.21cnjy.com/search.php?bigclass=downlist&dosearch=yes&srchtxt='}

    for kw in key_words:
        curr_website = 'gaokaowang'
        if curr_website == 'gaokaowang':
            download_gaokaowang_page(kw, website_url_dict[curr_website])
        elif curr_website == '21shiji':
            download_21shiji_page()
        else:
            pass
            # todo download other web


def input_key_word():
    while True:
        kw = input('Input Key Word:')
        download_gaokaowang_page(kw, 'http://tiku.gaokao.com/search/type0/')


# start
if __name__=='__main__':
    main()
    # input_key_word()