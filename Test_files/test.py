import json
from urllib.request import urlopen, Request
YEAR = 2014
url = f"https://raw.githubusercontent.com/GraphtyLove/KPMG-Challenge/master/assets/json/links_entreprises/links_entreprises_{YEAR}.json"
response = urlopen(url)
data = json.loads(response.read())
data = list(set(data))
data.sort()
print(data[0])


