import requests

# * --------- Scrap one file --------- *
url = 'https://statuten.notaris.be/costa_v1/api/costa-api/documents/24997'
r = requests.get(url)
with open(f'pdf/doc-24997', 'wb') as f:
    f.write(r.content)

# * --------- Scrap plenty of files --------- *
# for i in range(24997, 47000):
#     url = f'https://statuten.notaris.be/costa_v1/api/costa-api/documents/{i}'
#     r = requests.get(url)
#     with open(f'pdf/doc-{i}', 'wb') as f:
#         f.write(r.content)