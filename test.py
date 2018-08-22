import urllib.request
from time import sleep


from bs4 import BeautifulSoup

BASE_URL = 'https://www.avito.ru/sankt-peterburg/tovary_dlya_kompyutera/komplektuyuschie?s_trg=3&q=1080'


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


soup = BeautifulSoup(get_html(BASE_URL), 'html.parser')
work_item = soup.find('div', 'js-catalog_before-ads')
links_array = []
for each_div in soup.findAll('div',{'class':'item_table-header'}):
    source = each_div.find('a')
    links_array.append(source)
#for a in links_array:
#    print(soup.findNext('span', itemprop = "name"))
    #print(each_div(soup.find(('span',{'class':'price'}))))


for link in links_array:
   if ((('http://avito.ru' + link.get('href')) not in (links_array)) & (link.get('href').find('favorites') == -1)):
       links_array.append('http://avito.ru' + link.get('href'))
descript = work_item.findAll('div', 'about')
descript_array = []
for desc in descript:
    descript_array.append(desc)
print(descript_array)
print(links_array)