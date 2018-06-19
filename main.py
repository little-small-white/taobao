from spider import Spider
from mongo import Mongo

keyword = 'Python'
spider = Spider(keyword)
mongo = Mongo('taobao', keyword)  # 创建mogodb
print('start keyword:', keyword)
total_page = spider.search()  # 打开搜索页面
print('total page:', total_page)
for page in range(1, total_page + 1):
    html = spider.next_page(page)  # 根据页码获取搜索结果页面
    items = spider.parse(html)  # 提取数据
    ids = mongo.insert_many(items)  # 保存到mongodb中去
    print('current page:', page, 'save to mongo items:', len(ids))
