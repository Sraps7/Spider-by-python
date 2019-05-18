import requests
# from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup as bs
from selenium import webdriver
# import uuid
import os
# import winsound
# from tkinter import *
import time
from multiprocessing import Pool
from Tell_me_on_ending import tell_me_on_ending as tell_me

driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
headers = {
    'Cookie': 'UM_distinctid=16885736e00105-06cad551febe56-b781636-100200-16885736e014d; CNZZDATA1000465408=151875421-1548425514-https%253A%252F%252Fwww.baidu.com%252F%7C1548425514; CNZZDATA1000465515=383249325-1548425822-https%253A%252F%252Fwww.baidu.com%252F%7C1548425822; show_tip_1=0; display_mode=0; code_show=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Referer': 'https://manhua.dmzj.com/beatstars/62456.shtml'
}


def get_chapter(href, comic_name, comic_vol, my_task):
    print('run task %s (%s)...' % (my_task, os.getpid()))
    start = time.time()
    count_for_print = 1
    driver.get(href)
    # soup = bs(driver.page_source, 'lxml')
    total_page = bs(driver.page_source, 'lxml').select('select#page_select option')[-1].text[1:3]
    # print(type(soup.select('span#k_total')[0]))
    # print(total_page)
    for i in range (1, int(total_page) + 1):
        # print(href)
        pic_href = href + '#@page=' + str(i,)
        # print(pic_href)
        # time.sleep(5)
        driver.get(pic_href)

        # time.sleep(1)

        pic_soup = bs(driver.page_source, 'lxml')
        # print(soup)
        src = pic_soup.select_one('div#center_box img')['src']
        pic_src = 'https:' + src
        response = requests.get(pic_src, headers=headers)
        # print(src)
        if not os.path.exists("img"):
            os.mkdir("img")
        if not os.path.exists('img/' + comic_name):
            os.mkdir('img/' + comic_name)
        if not os.path.exists('img/' + comic_name + '/' + comic_vol):
            os.mkdir('img/' + comic_name + '/' + comic_vol)
        if not os.path.exists('img/' + comic_name + '/' + comic_vol + '/' + str(i) + '.jpg'):
            with open('img/' + comic_name + '/' + comic_vol + '/' + str(i) + ".jpg", 'wb') as fs:
                fs.write(response.content)
                print("download success!:" + comic_name + ' ' + comic_vol + ' ' + str(i) + ' ' + str(
                    count_for_print) + '/' + total_page)
        else:
            print("download has already be successful!:" + comic_name + ' ' + comic_vol + ' ' + str(i) + ' ' + str(
                count_for_print) + '/' + total_page)
        count_for_print = count_for_print + 1
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (my_task, (end - start)))


comic_name = 'Beastars'
home_url = 'https://manhua.dmzj.com/beatstars'
home_response = requests.get(home_url).text
home_soup = bs(home_response, 'lxml')
url_end = home_soup.select('div.cartoon_online_border ul li')
if __name__ == '__main__':
    # p = Pool(2)
    my_task = 1
    for i in range(127, len(url_end)):
        chapter_url = 'https://manhua.dmzj.com' + url_end[i].select_one('a')['href']
        comic_vol = url_end[i].select_one('a').text
        res_temp = requests.get(chapter_url)
        true_chapter_url = res_temp.url
        # driver.get(true_chapter_url)
        # total_page = bs(driver.page_source, 'lxml').select('select#page_select option')[-1].text[1:3]
        # p.apply_async(get_chapter, args=(true_chapter_url, comic_name, comic_vol, my_task))
        get_chapter(true_chapter_url, comic_name, comic_vol, my_task)
        my_task += 1
        # print(total_page)
    # driver.close()