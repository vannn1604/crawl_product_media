import scrapy
from collections import defaultdict
import re
from ..items import SpecItem


class SpecsSpider(scrapy.Spider):
    name = "spec"
    allowed_domains = ["www.gsmarena.com"]
    start_urls = ["https://www.gsmarena.com/makers.php3"]

    def parse(self, response):
        for a in response.xpath('//*[@id="body"]/div/div[2]/table/tr/td/a'):
            yield response.follow(
                a, callback=self.parse_brand, cb_kwargs={"brand": a.xpath("./text()").get()}
            )

    def parse_brand(self, response, brand):
        for product in response.xpath('//*[@id="review-body"]/div[1]/ul/li/a'):
            yield response.follow(
                product,
                callback=self.parse_specs,
                cb_kwargs={"name": product.xpath("./strong/span/text()").get(), "brand": brand},
            )

        for a in response.xpath('//a[@class="pages-next"]'):
            yield response.follow(a, callback=self.parse_brand, cb_kwargs={"brand": brand})

    def parse_specs(self, response, name, brand):
        specs = {}
        for i, table in enumerate(response.xpath('//*[@id="specs-list"]/table')):
            th = table.xpath("./tr[1]/th/text()").get()
            specs[th] = {}
            for j, tr in enumerate(table.xpath("./tr")):
                if i == 0 and j == 0:
                    td2 = tr.xpath("./td[2]/a/text()").get()
                else:
                    td2 = tr.xpath("./td[2]/text()").get()

                if td2 is not None:
                    td2.strip()
                td1 = tr.xpath("./td[1]/a/text()").get()
                if not td1:
                    td1 = "Other"
                else:
                    td1.strip()
                specs[th][td1] = td2
        scripts = response.xpath('//*[@id="body"]/div/script[1]/text()').getall()
        spec_ver = None
        for script in scripts:
            if "SPEC_VERSIONS" in script:
                script = re.sub("[\\\\\n]", "", script)
                match = re.search(r"\[.*\]", script)
                if match and match.group():
                    script = match.group()

        # a = re.findall(r"{(.*?)}", script)
        m = re.findall(r'"([^"]*)"', script)
        regex = r"{.*?}|(\w+)"
        matches = re.finditer(regex, script, re.MULTILINE)
        c = []
        for match in matches:
            if match.group(1):
                c.append(match.group(1))

        array = []
        for i, n in enumerate(m):
            if "href" in n:
                array.append({"key": i, "next_key": m[i + 1], "value": "" + n + m[i + 1]})

        for elmt in array:
            m[elmt["key"]] = elmt["value"]
        for elmt in array:
            m.remove(elmt["next_key"])

        spec_ver = {}
        for i, n in enumerate(m):
            if n in c:
                spec_ver[n] = {}
                for j in range(i + 1, len(m) - 1):
                    if m[j] in c:
                        break
                    if (j - i) % 2 == 1:
                        spec_ver[n][m[j]] = m[j + 1]

        if spec_ver:
            specs["SPEC_VERSIONS"] = spec_ver

        yield SpecItem(brand=brand, name=name, spec=specs)
        # for ver in spec_ver:  # a2220
        #     spec_follow_ver = specs
        #     for spec in spec_ver[ver]:  # sim

        #         for th in specs:
        #             for td in specs[th]:
        #                 if spec == td.lower():
        #                     spec_follow_ver[th][td] = spec_ver[ver][spec]
        #     yield {"brand": brand, "name": name, "version": ver, "specs": spec_follow_ver}


# dung regex de loc du lieu, push to db ko đc hết


"""
        item = defaultdict(list)
        item["brand"] = brand
        item["name"] = name
        item["specs"] = specs

        yield item

        for product in response.xpath('//*[@id="user-comments"]/div[4]/div[1]/ul/li[1]/a'):
            yield response.follow(
                product, callback=self.parse_reviews, cb_kwargs={"item": item},
            )

    def parse_reviews(self, response, item):
        for div in response.xpath('//div[@class="user-thread"]'):
            username = div.xpath("./ul[1]/li[1]/text()").get()
            if username is None:
                username = div.xpath("./ul[1]/li[1]/a/b/text()").get()
            # if not div.xpath("./p/span[1]"):
            #     parent_id = div.xpath("./@id").get()
            # elif div.xpath("./p/a/@href").get():
            #     parent_id = div.xpath("./p/a/@href").get()[1:]
            # else:
            #     parent_id = {
            #         "username": div.xpath("./p/span[1]/text()").get().split(",")[0],
            #         "time": div.xpath("./p/span[1]/text()").get().split(",")[1][1:],
            #         "content": div.xpath("./p/span[2]/text()").get(),
            #     }
            review = {
                # "id": div.xpath("./@id").get(),
                # "parent_id": parent_id,
                "username": username,
                "time": div.xpath("./ul[1]/li[3]/time/text()").get(),
                "content": div.xpath("./p/text()").get(),
                "rating": div.xpath("./ul[2]/li[1]/span[2]/text()").get(),
                "location": div.xpath("./ul[1]/li[2]/span/text()").get(),
            }

            item["reviews"].append(review)
        if not response.xpath('//a[@title="Next page"]'):
            # for i, review in enumerate(item["reviews"]):
            #     if type(review["parent_id"]) is dict:
            #         for j in range(i + 1, len(item["reviews"])):
            #             if (
            #                 item["reviews"][i]["parent_id"]["username"]
            #                 == item["reviews"][j]["username"]
            #                 and item["reviews"][i]["parent_id"]["time"]
            #                 == item["reviews"][j]["time"]
            #                 and item["reviews"][i]["parent_id"]["content"]
            #                 == item["reviews"][j]["content"]
            #             ):
            #                 item["reviews"][i]["parent_id"] = item["reviews"][j]["id"]
            #         if type(review["parent_id"]) is dict:
            #             review["parent_id"] = review["id"]
            yield item

        for a in response.xpath('//a[@title="Next page"]'):
            yield response.follow(
                a, callback=self.parse_reviews, cb_kwargs={"item": item},
            )
"""

