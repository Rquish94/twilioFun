import urllib3
import re

myDic = {}
def customdstFunc(dict):
    for i in dict:
        if destination.lower() in i:
            ret = (myDic[i])
            return ret
def customorgFunc(dict):
    for i in dict:
        if origin.lower() in i:
            out = (myDic[i])
            return out
def pairwise(it):
    it = iter(it)
    while True:
        yield next(it), next(it)

url = 'http://www.leonardsguide.com/us-airport-codes.shtml'
http = urllib3.PoolManager()
req = http.request('GET',url)
newText = str(req.data).replace('</span>','').replace('<span>','').replace('</i>','').replace('<i>','').lower()
urls = re.findall('<td>(.+?)</td>',newText,re.DOTALL)

for a, b in pairwise(urls):
    myDic[a] = str(b).upper()


origin = input('Please enter your origin airport\n')
if 'bradley' in origin:
    origin = 'hartford'
departMonth = input('Please enter your destination month (numeric)\n')
departDate = input('Please enter your destination date\n')
destination = input('Please enter your destination airport\n')
returnMonth = input('Please enter your return month (numeric)\n')
returnDate = input('Please enter your return date (numeric)\n')
#newOrg = origin.lower().split(' ')
newneworg = customorgFunc(myDic)
newnewdst = customdstFunc(myDic)
print('orgin = '+newneworg,departMonth,departDate+"\n")
print('dest = '+ newnewdst,returnMonth,returnDate+"\n")
# url = "http://google--flights.com/#/flights/BDL1902PBI2"
# http = urllib3.PoolManager()
# req = http.request('GET',url)
# newText = str(req.data).replace('><','\n')
# urls = re.findall('a href="/url(.+?)"',newText,re.DOTALL)
# count = 0
# for i in urls:
#     if len(range(count)) < 10:
#         lookupURLS.append(i)
#         count=+1
#     else:
#         continue
# print(lookupURLS)
#
