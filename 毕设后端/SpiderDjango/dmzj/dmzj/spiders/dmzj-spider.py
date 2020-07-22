import scrapy
import re
import json

from dmzj.items import DmzjItem


class DMZJSpider(scrapy.Spider):
    name = "DMZJ"
    allowed_domains = ['m.dmzj.com']
    start_urls = ['http://m.dmzj.com']

    def __init__(self, manhua_url = '', manhua_name = '', *args, **kwargs):
        self.url = manhua_url
        self.manhua_name = manhua_name

    def start_requests(self):
        yield scrapy.http.Request(url=self.url, callback=self.first_url_parse)

    #找到漫画在移动端的url地址
    def first_url_parse(self, response):
        url = 'https://m.dmzj.com/info/%s.html'
        if 'info' in self.url:
            #若info存在，获取漫画名
            manhua_id_1 = re.split('/', self.url)[-1]
            manhua_id = re.split(r'\.', manhua_id_1)[0]
        else:
            manhua_id_1 = response.xpath('//head/script/text()').get()
            manhua_id = re.search(r'.*?g_current_id = "(.*?)";.*', manhua_id_1).group(1)
        main_url = url % manhua_id
        yield scrapy.http.Request(url=main_url, callback=self.parse_total)

    def parse_total(self, response):
        #拿到第一个script标签内的内容，为id、name等信息
        catalog = response.xpath('//body/script[@type="text/javascript"]/text()').getall()[1]
        catalog = re.sub(r'},{"title":.*?,"data":\[(.*?)\]', '', catalog)
        #每话地址
        catalog_list = json.loads(re.search(r'"data":(.*?)}]\);.*',catalog).group(1))
        data_list = []

        for ls in catalog_list:
            #url内包含两个加密数字
            detail_url = 'https://m.dmzj.com/view/%s/%s.html' % (ls['comic_id'],ls['id'])
            yield scrapy.http.Request(url=detail_url, callback=self.parse_detail)


    def parse_detail(self, response):
        #章节名
        title = response.xpath('//a[@class="BarTit"]/text()').get()
        #每页的url地址
        pic_urls = response.xpath('//body/script[@type="text/javascript"]/text()').getall()[1]
        pic_urls = json.loads(re.search(r'.*?"page_url":(.*?),"chapter_type".*', pic_urls).group(1))
        item = DmzjItem(pic_urls=pic_urls, title=title, big_title=self.manhua_name)
        yield item