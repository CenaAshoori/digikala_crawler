# Digikala Products Crawler


## Quick Start :
```bash
    pip install scrapy
```
Then
```bash
    scrapy crawl product -o result.json
```
And tap Enter to set default value .

Now in json file you can see all products that are simillar with the defualt product that i save in to the app. 
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

Scrapy automaticly won't crawl repeated links.

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
### For changing the result and crawl specefic Produc .
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
and declear the depth of search
```python 
self.product_per_page = int (input("Enter number of product per page\n>>") or 16)
self.depth = int(input("Enter depth of crawling \n>>") or 10)
```

and for normalization on data we'll convert persian number to en and remove camma and we add more or use some liberary on the web .
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
with depth variable in the method we have access to the depth of the crawling and Scrapy don't exceed that range.
```python 
def parse(self, response):
    depth = response.meta.get('depth')
    category = response.xpath('//*[@id="content"]/div[1]/div/article/section[1]/div[1]/div/div/div/a[2]/text()')
    name_en = response.xpath('//*[@id="content"]/div[1]/div/article/section[1]/div[2]/div[2]/span/text()')
```
for having more cleaner code :D get category and name_en outside of yeild and also this feild can be blank in some products 

---
for digikala this fields have this XPATH address.

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
and with this piece of code we can understand that current depth wouldn't excced from specified depth and if it wasn't that we calculate the related products.
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
with selecting this area we have access to all product in this section but we need the `<a>` Tag of these product so if we have //a at the end of above code we have access to all of the products link.

```python
product_links = response.xpath('//*[@id="content"]/div[1]/div/div[3]/div[2]/div/div/div//a')

for item in product_links:
    links.append(self.url + "/".join(item.attrib["href"].split("/")[:3]))

```

****


