import scrapy


class ProductSpider(scrapy.Spider):
    def __init__(self):
        url = input(
"""
-Enter URL of one of the Digikala's Product
OR
-Just press Enter to get sample Result
>>>""")
        if url != "":
            self.start_urls = [url]
        self.product_per_page = int (input("Enter number of product per page\n>>") or 16)
        self.depth = int(input("Enter depth of crawling \n>>") or 10)

    fa_num = {"۰": "0", "۱": "1", "۲": "2", "۳": "3", "۴": "4", "۵": "5", "۶": "6", "۷": "7", "۸": "8", "۹": "9",",":""}
    name = "product"
    url = "https://www.digikala.com"
    start_urls = [
        "https://www.digikala.com/product/dkp-4149254",
    ]

    def convert_num(self, num_str):
        ans = ""
        for char in num_str:
            temp = self.fa_num.get(char)
            if temp != None:
                ans += temp
            else:
                ans += char
        return int(ans)

    def parse(self, response):
        depth = response.meta.get('depth')
        category = response.xpath('//*[@id="content"]/div[1]/div/article/section[1]/div[1]/div/div/div/a[2]/text()')
        name_en = response.xpath('//*[@id="content"]/div[1]/div/article/section[1]/div[2]/div[2]/span/text()')
        yield {
            "name": response.xpath('//*[@id="content"]/div[1]/div/article/section[1]/div[1]/div/h1/text()').get().strip(),
            "en-name": name_en.get().strip() if len(name_en) else "",
            "price": self.convert_num(response.xpath('//*[@id="content"]/div[1]/div/article/section[1]/div[2]/div[3]/div/div[1]/div[1]/div[11]/div[2]/div/text()').get().strip()) ,
            "category": category.get().strip() if len(category) else "",
            "url": response.url,

        }
        if depth < self.depth:
            product_links = response.xpath('//*[@id="content"]/div[1]/div/div[3]/div[2]/div/div/div//a')
            links = []
            product_links = product_links if len(product_links) < self.product_per_page else product_links[
                                                                                             :self.product_per_page]
            for item in product_links:
                links.append(self.url + "/".join(item.attrib["href"].split("/")[:3]))

            yield from response.follow_all(links, callback=self.parse)

