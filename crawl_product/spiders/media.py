import scrapy
from ..items import MediaItem


class MediaSpider(scrapy.Spider):
    name = "media"
    allowed_domains = ["www.gsmarena.com"]
    start_urls = ["https://www.gsmarena.com/apple_iphone_11_pro_max-pictures-9846.php"]

    def parse(self, response):
        item = MediaItem()
        img_urls = []
        for img in response.xpath('//*[@id="pictures-list"]/img'):
            a = img.xpath("./@src").get()
            if not a:
                continue
            img_urls.append(img.xpath("./@src").get())
        item["image_urls"] = img_urls
        return item
