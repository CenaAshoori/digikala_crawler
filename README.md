# Digikala Products Crawler

در پوشه را مطالعه کنید [pdf](https://github.com/CenaAshoori/digikala_crawler/blob/main/result%20feed/97149078-%D8%AA%D9%88%D8%B6%DB%8C%D8%AD%D8%A7%D8%AA%20%D9%BE%D8%B1%D9%88%DA%98%D9%87.pdf) برای توضیحات فارسی

## Quick Start :
```bash
    pip install scrapy
```
Then Clone
```bash
   git clone git@github.com:CenaAshoori/digikala_crawler.git
```
And Then
```bash
    scrapy crawl product -o result.json
```
And tap Enter to set the default value .

Now in the json file you can see all products that are similar with the default product that i save that link inside the code. 
```json 
[
	{
		"name": "کفش راحتی مردانه  مدل Gazelle",
		"price": 1240000,
		"category": "non category",
		"url": "https://www.digikala.com/product/dkp-510849"
	},
	{
		"name": "کفش راحتی مردانه مدل Stan Smith",
		"price": 2050000,
		"category": "non category",
		"url": "https://www.digikala.com/product/dkp-767696"
	}
]
```

Scrapy automatically won't crawl repeated links.

for getting data with 

## Json
```bash
    scrapy crawl product -o result.json
```
## JL
```bash
    scrapy crawl product -o result.jl
```
## CSV
```bash
    scrapy crawl product -o result.csv
```
## XML
```bash
    scrapy crawl product -o result.xml
```

---
### For changing the result and crawl specific Product .
```python 
class ProductSpider(scrapy.Spider):
    def __init__(self):
        url = input(
"""
-Enter URL of one of the Digikala's Product
OR
-Just press Enter to get sample Result
>>>""")
        if url != "":
            self.start_urls.clear()
            self.start_urls.append(url)

```
and declare the depth of search
```python 
self.product_per_page = int (input("Enter number of product per page\n>>") or 16)
self.depth = int(input("Enter depth of crawling \n>>") or 10)
```

and for normalization on data we'll convert persian numbers to en and remove commas and we add more or use some library on the web .
```python 
fa_num = {"۰": "0", "۱": "1", "۲": "2", "۳": "3", "۴": "4", "۵": "5", "۶": "6", "۷": "7", "۸": "8", "۹": "9" , ",":""}
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
    return ans

```
---
With a depth variable in the method we have access to the depth of the crawling and Scrapy doesn't exceed that range.
```python 
def parse(self, response):
    depth = response.meta.get('depth')
    category = response.xpath('//*[@id="content"]/div[1]/div/article/section[1]/div[1]/div/div/div/a[2]/text()')
    name_en = response.xpath('//*[@id="content"]/div[1]/div/article/section[1]/div[2]/div[2]/span/text()')
```
for having more cleaner code :D get category and name_en outside of yield and also this field can be blank in some products 

---
For digikala these fields have this XPATH address.

```python 
yield {

"name": response.xpath('//*[@id="content"]/div[1]/div/article/section[1]/div[1]/div/h1/text()').get().strip(),

"en-name": name_en.get().strip() if len(name_en) else "",

"price": self.convert_num(response.xpath('//*[@id="content"]/div[1]/div/article/section[1]/div[2]/div[3]/div/div[1]/div[1]/div[11]/div[2]/div/text()').get().strip()),

"category": category.get().strip() if len(category) else "",

"url": response.url,

    }
```
---
and with this piece of code we can understand that current depth wouldn't exceed from specified depth and if it wasn't that we calculate the related products.
```python
if depth < self.depth:
    product_links = response.xpath('//*[@id="content"]/div[1]/div/div[3]/div[2]/div/div/div//a')
    links = []
    product_links = product_links if len(product_links) < self.product_per_page else product_links[
                                                                                     :self.product_per_page]
    for item in product_links:
        links.append(self.url + "/".join(item.attrib["href"].split("/")[:3]))

    yield from response.follow_all(links, callback=self.parse)

```
![digikala products picture](result%20feed/pic.jpg)


```xpath 
//*[@id="content"]/div[1]/div/div[3]/div[2]/div/div/div
```
With selecting this area we have access to all products in this section but we need the `<a>` Tag of these products so if we have //a at the end of above code we have access to all of the products link.

```python
product_links = response.xpath('//*[@id="content"]/div[1]/div/div[3]/div[2]/div/div/div//a')

for item in product_links:
    links.append(self.url + "/".join(item.attrib["href"].split("/")[:3]))

```

****



