# 淘宝搜索接口爬虫
可根据自定义 **关键字** 使用Selenium调用Chrome获取搜索结果。

# spider.py 使用Selenium驱动Chrome获取搜索结果，提取搜索结果
- spider.try_time 处理Selenium expected_condiction 超时异常重试
- Spider(keyword) 传入keyword构建spider
- Spider.search() 调用Chrome获取淘宝首页，键入keyword，获取搜索结果总页数
- Spider.next_page(page) 根据传入的页面对结果也进行翻页处理，返回对应结果页面html
- Spider.parse(html) 使用BeautifulSoup解析结果页面，利用生成器返回解析结果

# mongo.py 对mongodb进行简单的封装
- Mongo(db, collection) 根据db和collection构建mongodb客户端
- Mongo.insert(document) 插入一条记录
- Mongo.insert_many(documents) 批量插入记录

# main.py 爬虫启动模块
实例化Spider，调用Spider的搜索、翻页、提取数据接口，实例MongodbClient，将提取到的结果保存到Mongodb中去。
可根据需要修改Mongodb的连接信息，或者去掉保存到Mongodb。
