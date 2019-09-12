# import json
# from urllib.request import urlopen, Request
# YEAR = 2014
# url = f"https://raw.githubusercontent.com/GraphtyLove/KPMG-Challenge/master/assets/json/links_entreprises/links_entreprises_{YEAR}.json"
# response = urlopen(url)
# data = json.loads(response.read())
# data = list(set(data))
# data.sort()
# print(data[0])
#
l = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
for i, k in enumerate(l[5:]):
    print('i+5 ', i+5)
    print(k)

