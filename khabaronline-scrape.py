# -*- coding: utf-8 -*-



import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas as pd

def scrap_year():
    page = 0
    scraped_data = []
    url_list = []
    done = False
    last_url = ''

    while True:
        page += 1

        main_page_url = f"https://www.hamshahrionline.ir/page/archive.xhtml?wide=0&ms=0&pi={page}"

        html = requests.get(main_page_url).text

        soup = BeautifulSoup(html, features='lxml')

        linksContainer = soup.find_all('section', { "id" : "box16" })[0]
        links = linksContainer.find_all("div")

        if done: break

        for index, link in enumerate(tqdm(links)):
            tag_a = link.find_all("a")[0]
            page_url = 'https://www.hamshahrionline.ir' + tag_a['href']
            print(page_url)
            url_list.append(page_url)

            if index == 0:
                if (last_url == page_url):
                    print(last_url, page_url)
                    done = True
                    break;
                last_url = page_url

            try:
                article = Article(page_url)
                article.download()
                article.parse()
                scraped_data.append({'url': page_url, 'text': article.text, 'title': article.title})
            except:
                print(f"Failed to process page: {page_url}")

    df = pd.DataFrame(scraped_data)
    df.to_csv('D:/export.csv')


scrap_year()

