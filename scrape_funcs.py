# __author__ = 'ktc312'
#  -*- coding: utf-8 -*-
# coding: utf-8
import urllib.request
from bs4 import BeautifulSoup
import os
import csv
import time
from socket import *


data_path = os.path.dirname(os.path.abspath(__file__)) + '/data/'
base_url = str('http://visadoor.com/greencards/index')


def raw_data_rows_to_csv(list_data, file_name):
    with open(data_path + file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerows(list_data)


def get_country_list():
    index_page = BeautifulSoup(urllib.request.urlopen(base_url, data=None, timeout=1), "html.parser")
    country_list = [str(x.text).replace(" ", "+") for x in index_page.find("select", {"name": "country"})
                    .find_all('option')]
    country_list.pop(0)
    return country_list


def get_cases_found(country_name):
    cases_found_in_page = 0
    search_term = "?&submit=Search&country=" + country_name
    soup = BeautifulSoup(urllib.request.urlopen(base_url + search_term, data=None), "html.parser")
    cases_found_class = soup.findAll("div", {"class": "col-sm-5"})
    for div in cases_found_class:
        cases_found_in_page = int(str(div).split('<h4>')[1].split(' ')[3])
    print("{} has {} cases".format(country_name, cases_found_in_page))
    return cases_found_in_page


def get_page_count(cases_count):
    if cases_count <= 1000:
        page_count = 1
    else:
        page_count = (cases_count/1000) + 1
    return page_count


def name_and_page(country_list):
    output = {}
    fail_list = []
    for country_name in country_list:
        for _ in range(10):
            try:
                output[country_name] = get_page_count(get_cases_found(country_name))
                break
            except timeout:
                print('------------------fail at {}------------------'.format(country_name))
                fail_list.append(country_name)
                time.sleep(3)

    return output, fail_list


def scrape_data(country_name, page_count):
    i = 1
    raw_data = []
    while i <= page_count:
        while True:
            try:
                print('starting page {} for {}'.format(i, country_name))
                search_term = "?country=" + country_name + '&page=' + str(i) + '&submit=Search'
                data_page = BeautifulSoup(urllib.request.urlopen(base_url + search_term, data=None, timeout=5),
                                          "html.parser")

                table = data_page.find('table', attrs={'class': 'table table-bordered table-striped table-hover'})
                rows = table.findAll('tr')
                iter_rows = iter(rows)
                next(iter_rows)
                for row in iter_rows:
                    cols = row.findAll('td')
                    cols = [ele.text.strip() for ele in cols]
                    for col in cols:
                        raw_data.append(col)
                time.sleep(2)
                print(int(len(raw_data)/7))
                print('ending page {} for {}'.format(i, country_name))
                i += 1
                break
            except timeout:
                pass
            except AttributeError:
                print('abort this page')
                i += 1
                break

    i = 0
    raw_data_rows = []
    while i < len(raw_data):
        raw_data_rows.append(raw_data[i:i + 7])
        i += 7
    raw_data_rows_to_csv(raw_data_rows, country_name+'_data.csv')
    loop_through = True
    return loop_through
