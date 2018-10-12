import bs4
import csv
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
# opens up web connection to LTC facilities, grab page, close client
my_url = 'https://www.in.gov/isdh/reports/QAMIS/ltcdir/wdirltc.htm'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
# parse + find text
page_soup = soup(page_html, "html.parser")
data = page_soup.find('pre')

# clean up data
lines = data.text.split('\r\n')
lines = list(map(str.strip, lines))
# initialization for data cleaning
l, l2 = [], []
to_replace = ['Administrator: ', 'Tel: ', 'Fax: ',
              'License Number : ', 'Lic Expire Date : ', 'Bed Capacity: ', ' SNF/NF', ' SNF', ' NF', ' NCC', ' RES']
# clean up bed information
lines = [l.split(',  ') if l.endswith('RES') else l for l in lines]
lines = [i for b in map(lambda x:[x] if not isinstance(x, list) else x, lines) for i in b]
# removing unnecessary labels from data and organizing into list of rows
for line in lines:
    for t in to_replace:
        line = line.replace(t, '')
    if line != "":
        l2.append(line)
    else:
        l.append(l2)
        l2 = []
# remove header information
del l[:2]
# intialize for csv writing
headers = "Hospital,Facility Name,Address,City,Administrator,Telephone,Fax,License,License Expiration,Bed Capacity,SNF,NF,SNF / NF,NCC,RES\n"
filename = 'ltc_facilities.csv'
# write to csv file
with open(filename, "w") as f:
    f.write(headers)
    writer = csv.writer(f)
    writer.writerows(l)
