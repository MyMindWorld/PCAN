#!/usr/bin/env python3.5
# -*- encoding: utf-8 -*-

import csv
# для python 2.7 - urllib2
# import urllib2
# import requests

# для python 3.3 - urllib.request
import urllib.request
from time import sleep

from bs4 import BeautifulSoup

# BASE_URL = 'https://www.avito.ru/sankt-peterburg/tovary_dlya_kompyutera/komplektuyuschie?q=gtx%201080&sgtd=21'
BASE_URL = 'https://www.avito.ru/sankt-peterburg/tovary_dlya_kompyutera/komplektuyuschie?s_trg=3&q=1080'


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def get_page_count(html):
    # 'html.parser' для совместмости с debian 8. без этого на debian не работает. на ubuntu нормально.
    soup = BeautifulSoup(html, 'html.parser')
    # print (soup)
    paggination = soup.find('div', class_='pagination-pages clearfix')
    print(paggination)
    # основаная строка для парсинга количества страниц
    if paggination is None:
        return 2
    return int(paggination.find_all('a', href=True)[-1]['href'][-3:])


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    work_item = soup.find('div', class_='js-catalog_before-ads')
    links = work_item.findAll('a')
    links_array = []
    for link in links:
        if ((('http://avito.ru' + link.get('href')) not in (links_array)) & (link.get('href').find('favorites') == -1)):
            links_array.append('http://avito.ru' + link.get('href'))
    descript = work_item.findAll('div', 'about')
    descript_array = []
    for desc in descript:
        descript_array.append(desc)
    print(descript_array)
    print(links_array)
    description = work_item.find_all('div', class_='description')
    print("here")
    data = []
    for item in description:
        data.append({
            'title': item.a.text,
            'price': item.find('span', class_='price').text.strip()
            # 'type': item.find('div', class_='data').p.text.strip(),
        })
    print(data)
    print('end')
    return data


def save(projects, path):
    with open(path, 'w') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(('Name', 'Price'))  # , 'Desc'))

        writer.writerows(
            # ".encode('utf-8')" нужен для правильной интерпретации unicode
            (project['title'].encode('utf-8'),
             project['price'].encode('utf-8'),
             # project['type'].encode('utf-8'),
             ) for project in projects
        )


def main():
    total_pages_words = get_page_count(get_html(BASE_URL))

    print('Всего найдено %d страниц...' % total_pages_words)

    projects = []
    try:
        for page in range(1, total_pages_words + 1):
            print('Парсинг %d%% (%d/%d)' % (int(float(page) / float(total_pages_words) * 100), page, total_pages_words))
            projects.extend(parse(get_html(BASE_URL + "?p=%d" % page)))
            sleep(10)
    finally:
        print('Сохранение...')
        save(projects, 'projects_all.csv')

    # печать для теста
    # for item in projects:
    #   print(item['title'].encode('utf-8'))
    #  print(item['price'].encode('utf-8'))


if __name__ == '__main__':
    main()
