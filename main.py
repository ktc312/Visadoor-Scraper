# __author__ = 'ktc312'
#  -*- coding: utf-8 -*-
# coding: utf-8
import scrape_funcs as sf
import time

country_list = sf.get_country_list()
country_name_and_page, fail_list = sf.name_and_page(country_list)


def main(name_and_page):
    for country_name, page_count in name_and_page.items():
        while True:
            job_done = sf.scrape_data(country_name, page_count)
            if job_done:
                print('{} data complete'.format(country_name))
                break
            else:
                print('Retry scraping {} data'.format(country_name))
                time.sleep(1)
                pass


if __name__ == '__main__':
    main(country_name_and_page)
