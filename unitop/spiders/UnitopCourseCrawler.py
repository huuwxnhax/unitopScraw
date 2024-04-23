import scrapy
from unitop.items import UnitopItem

class UnitopCourseSpider(scrapy.Spider):
    name = "UnitopAppCrawler"
    allowed_domains = ["unitop.vn"]

    def start_requests(self):
        yield scrapy.Request(url='https://unitop.vn/', callback=self.parse)
        
    def parse(self, response):
        courseList = response.xpath('//div[@class="box-body"]/descendant::ul/li/div/a/@href').getall()
        for courseItem in courseList:
            item = UnitopItem()
            item['courseUrl'] = response.urljoin(courseItem)
            request = scrapy.Request(url = response.urljoin(courseItem), callback=self.parseCourseDetailPage)
            request.meta['datacourse'] = item
            yield request
            
    def parseCourseDetailPage(self, response):
        item = response.meta['datacourse']
        item['coursename'] = response.xpath('normalize-space(string(//h1))').get()
        item['lecturer'] = response.xpath('normalize-space(string(//a[@class="mentor"]))').get()
        item['intro'] = response.xpath('normalize-space(string(//div[@class="col-12"]/p[@class="course-desc"]))').get()
        item['describe'] = response.xpath('normalize-space(string(//div[@class="info-body"]/p))').get()

        item['votenumber'] = response.xpath('normalize-space(string(//span[@class="num-vote"]))').get()
        item['rating'] = response.xpath('normalize-space(string(count(//div[@class="show-star"]/i[contains(@class, "fas fa-star")])))').get()
        item['oldfee'] = response.xpath('normalize-space(string(//span[@class="old-fee"]))').get()
        item['newfee'] = response.xpath('normalize-space(string(//span[@class="new-fee"]))').get()
        item['lessonnum'] = response.xpath('normalize-space(string(//ul[@id="course-includes"]/li))').get()
        
        yield item
