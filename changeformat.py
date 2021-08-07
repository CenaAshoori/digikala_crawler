import sys
import json
f = open(f"{sys.path[0]}/product.json")

js = json.load(f)

print(js)
