# 2019/07/26

import os
import requests
from lxml import html

def scrape(save_path):
    print('[INFO] Setting up dailymirror scraper\n')
    i = 0
    href = 'http://www.dailymirror.lk/latest-news/342'

    # create save path if not exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # get 30 news articles
    while i < 2:
        # open the web page
        r = requests.get(href)
        page = html.fromstring(r.content)

        # get all the news story links from the front page
        hrefs = page.xpath('//div[@class="top-header-sub"]/div[@class="row"]/div[@class="col-md-8"]/a/@href')

        for url in hrefs:
            if i < 2:
                # open specific news story
                r2 = requests.get(str(url))
                page2 = html.fromstring(r2.content)

                # get title and content of the news article
                title = page2.xpath('//header[@class="inner-h"]/h1/text()')
                text = page2.xpath('//header[@class="inner-content"]/p/text()')
                
                # save the news article
                file = open('{}/dailymirror{}.txt'.format(save_path, i+1), 'w', encoding="utf-8")
                file.write(title[0])
                file.write('\n')
                for para in text:
                    file.write(para)
                file.close()

                print('[INFO] file {} scraped'.format(i+1))
                i += 1
    print('[INFO] (dailymirror) -> Task Complete\n\n')
