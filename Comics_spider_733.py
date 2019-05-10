#  chongmeng733.py与simple_chongmeng.py的结合版本
#  获取目录里每卷的链接地址，找到图片重定向后的网址
#  之后按照重定向后网址的规律直接定位所有该卷图片的真实地址
#  速度比chongmeng733.py要快，因为只需要每卷首页进行一次selemium，而不需要如以前每卷的每张都进行selenium

import requests
# from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup as bs
from selenium import webdriver
# import uuid
import os
import winsound
from tkinter import *
from multiprocessing import Pool
import time


driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
# request_retry = HTTPAdapter(max_retries=3)


def tell_me_on_ending():
    root = Tk()
    root.wm_attributes('-topmost', True)  # 窗口置顶
    root.title('给飘看的提醒')
    root.geometry('300x300')
    root.resizable(width=True, height=True)
    lable1 = Label(root, text='程序运行完毕啦', bg='blue', font=('黑体', 20), width=28, height=3)
    lable1.pack(side=LEFT)
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    root.mainloop()


def download_pic(pre_str_of_url, last_num_of_url, total_page, comic_name, comic_vol):
    count_for_print = 1
    for page_num in range(last_num_of_url, last_num_of_url + total_page):
        pic_url = pre_str_of_url + str(page_num) + '.jpg'
        # pic_url = 'http://img_733.234us.com/img/05/07/22/57061.jpg'
        response = requests.get(pic_url)
        if not os.path.exists("img"):
            os.mkdir("img")
        if not os.path.exists('img/' + comic_name):
            os.mkdir('img/' + comic_name)
        if not os.path.exists('img/' + comic_name + '/' + comic_vol):
            os.mkdir('img/' + comic_name + '/' + comic_vol)
        with open("img/" + comic_name + '/' + comic_vol + '/' + str(page_num) + ".jpg", 'wb') as fs:
            fs.write(response.content)
            print("download success!:" + comic_name + ' ' + comic_vol + ' ' + str(page_num) + ' ' + str(count_for_print) + '/' + str(total_page))
        count_for_print = count_for_print + 1


def get_chapter(href, comic_name, comic_vol, my_task):
    print('run task %s (%s)...' %(my_task, os.getpid()))
    start = time.time()
    driver.get(href)
    soup = bs(driver.page_source, 'lxml')
    total_page = int(soup.select('span#k_total')[0].text)
    # print(type(soup.select('span#k_total')[0]))
    # print(total_page)
    pic_href = soup.select_one('table#qTcms_Pic_middle img').attrs['src']
    res_pic = requests.get(pic_href)
    true_pic_href = res_pic.url
    last_num = int(true_pic_href[-10:-4])
    pre_str = true_pic_href[:-10]
    download_pic(pre_str, last_num, total_page, comic_name, comic_vol)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (my_task, (end - start)))


#  下载漫画步骤：
#  打开网站，搜索到需要下载的漫画的章节目录界面，更改漫画名称，写入该url
#  选择下载的章节（左上到右下次序排列）填入下面的for循环

comic_name = 'JOJO_第七部'
url = 'https://www.733.so/mh/8435/'
res = requests.get(url)
soup = bs(res.content, 'lxml')
chapter_wanted = soup.select('ul#mh-chapter-list-ol-0 li')
from_end_to_begin = 79

# def process_begin(href):
#     for i in range(28 + 5, 52):
#         pos = from_end_to_begin - i
#         href = 'https://www.733.so' + chapter_wanted[pos].select('a')[0]['href']
#         comic_vol = chapter_wanted[pos].select('a p')[0].text  # print(href)
#         # if not os.path.exists("img"):
#         #     os.mkdir("img")
#         # if not os.path.exists('img' + '/VOL' + str(x)):
#         #     os.mkdir('img' + '/VOL' + str(x))
#         # posit = 'img/VOL' + str(x)
#         # x = x - 1
#         get_chapter(href, comic_name, comic_vol)

if __name__ == '__main__':
    p = Pool(4)
    my_task = 1
    for i in range(28 + 19, 52):
        pos = from_end_to_begin - i
        href = 'https://www.733.so' + chapter_wanted[pos].select('a')[0]['href']
        comic_vol = chapter_wanted[pos].select('a p')[0].text  # print(href)
        p.apply_async(get_chapter, args=(href, comic_name, comic_vol, my_task))
        my_task = my_task + 1
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

    tell_me_on_ending()