import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def try_again(func):
    '''selenium expected_conditions 超时异常处理 最多尝试5次'''
    def wrapper(*args, **kwargs):
        for i in range(5):
            try:
                return func(*args, **kwargs)
            except TimeoutException as e:
                print(e, func.__name__, i, 'try again.')
                return func(*args, **kwargs)
        else:
            raise Exception('error...')
    return wrapper


class Spider:

    def __init__(self, keyword='Python'):
        self.keyword = keyword
        self.browser = webdriver.Chrome()
        self.until = WebDriverWait(self.browser, 10).until

    @try_again
    def search(self):
        '''获取淘宝首页 键入关键字搜索 返回搜索结果总页数'''
        self.browser.get('https://www.taobao.com')
        input_text = self.until(EC.presence_of_element_located((By.ID, 'q')))  # 搜索输入框
        button = self.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input_text.send_keys(self.keyword)
        button.click()
        page = self.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        return int(re.findall('\d+', page.text)[0])

    @try_again
    def next_page(self, page):
        '''根据page对搜索结果页面进行翻页 返回当前page的html'''
        input_text = self.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        button = self.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input_text.clear()
        input_text.send_keys(str(page))
        button.click()
        self.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page)))
        return self.browser.page_source

    def parse(self, html):
        '''解析 提取数据'''
        root = BeautifulSoup(html, 'lxml')
        items = root.select('#mainsrp-itemlist .m-itemlist .items > .item')
        for item in items:
            try:
                price = item.select_one('.price > strong').text
                cover = item.select_one('.J_ItemPic.img')['src']
                deal_cnt = item.select_one('.deal-cnt').text.rstrip('人付款')
                a = item.select_one('div.title > a')
                title = a.text.strip()
                link = a['href']
                yield {
                    'price': price,
                    'cover': cover,
                    'deal_cnt': deal_cnt,
                    'title': title,
                    'link': link,
                }
            except Exception as e:
                print(e, item)

    def __del__(self):
        '''退出时 关闭浏览器'''
        self.browser.close()
