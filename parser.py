# -*- coding: utf-8 -*-

import csv
import re
import urllib.request
from time import sleep
from transliterate import translit, get_available_language_codes
from bs4 import BeautifulSoup
from collections import OrderedDict

BASE_URL = 'https://www.avito.ru/sankt-peterburg/tovary_dlya_kompyutera/komplektuyuschie?pmax=25000&pmin=15000&s=1&s_trg=3&q=1080'
data = []

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()
def getKey(item):
    return item[1]

def get_page_count(html):
    # 'html.parser' для совместмости с debian 8. без этого на debian не работает. на ubuntu нормально.
    soup = BeautifulSoup(html, 'html.parser')
    # print (soup)
    paggination = soup.find('div', class_='pagination-pages clearfix')
    print(paggination)
    if paggination is None:
        return 1
    return int(paggination.find_all('a', href=True)[-1]['href'][-3:])


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    work_item = soup.find('div', class_='js-catalog_before-ads')
    links = work_item.findAll('a')
    links_array = []
    for link in links:
        if ((('http://avito.ru' + link.get('href')) not in (links_array)) & (link.get('href').find('favorites') == -1)):
            links_array.append('http://avito.ru' + link.get('href'))
    description = soup.findAll('div', {'class': 'item_table-header'})

    for item in description:
        data.append({
            'Name': item.a.text,
            'Price': str(''.join(re.findall(r'(\d+)',item.find('span', class_='price').text.strip()))),
            'Link': 'www.avito.ru'+item.find('a', href=re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
        })
    print(data)
    #sorted(data.values())
    '''for test in data: #Для тестового построчного вывода обьявлений
        print(test)
    print('end')'''
    return data


def save(projects, path):
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(('Name', 'Price', 'Link'))

        writer.writerows(
            (translit(project['Name'], 'ru', reversed=True),
             translit(project['Price'], 'ru', reversed=True),
             translit(project['Link'], 'ru', reversed=True),
             ) for project in projects
        )



def main():
    total_pages_words = get_page_count(get_html(BASE_URL))

    print('Всего найдено %d страниц...' % total_pages_words)

    projects = []
    try:
        for page in range(1, total_pages_words + 1):
            print('Парсинг %d%% (%d/%d)' % (int(float(page) / float(total_pages_words) * 100), page, total_pages_words))
            if total_pages_words == 1:
                projects.extend(parse(get_html(BASE_URL)))
                sleep(10)
            else:
                projects.extend(parse(get_html(BASE_URL + "?p=%d" % page)))
                sleep(10)
    finally:
        print('Сохранение...')
        save(projects, 'projects_all.csv')


if __name__ == '__main__':
    main()
