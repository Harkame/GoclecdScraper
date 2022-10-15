import requests
from bs4 import BeautifulSoup
import os

SEARCH_URL = 'https://www.goclecd.fr/catalogue/search-'

class SearchResult():
    def __init__(self):

        self.title = None
        self.price = 0.0
        self.symbol = None
        self.href = None

    def __str__(self):
        str = ''

        str += f'Title : {self.title}'
        str += os.linesep

        str += f'price : {self.price} {self.symbol}'
        str += os.linesep

        str += f'href : {self.href}'
        str += os.linesep

        return str


class Offers():
    def __init__(self):
        self.title = None
        self.price = 0.0
        self.symbol = None
        self.coupon = None
        self.price_without_coupon = 0.0
        self.edition = None
        self.review_count = 0
        self.href = None

    def __str__(self):
        str = ''

        str += f'Title : {self.title}'
        str += os.linesep

        str += f'Price : {self.price} {self.symbol}'
        str += f'Price without coupon : {self.price_without_coupon} {self.symbol}'
        str += os.linesep

        str += f'Coupon : {self.coupon}'
        str += os.linesep

        str += f'Edition : {self.edition}'
        str += os.linesep

        str += f'Review count : {self.review_count}'
        str += os.linesep

        str += f'href : {self.href}'
        str += os.linesep

        return str


class GoclecdScraper():
    def __init__(self):
        pass

    def get_offers(self, url):
        content = requests.get(url).content

        page = BeautifulSoup(content, 'lxml')

        offer_tags = page.find_all('div', {'class': 'offers-table-row x-offer'})

        offers = []

        for offer_tag in offer_tags:
            print(offer_tag)

        return offers


    def search(self, search):
        content = requests.get(SEARCH_URL + search.replace(' ', '+')).content

        page = BeautifulSoup(content, 'lxml')

        result_tags = page.find_all('li', {'class' : 'search-results-row'})

        search_results = []

        for result_tag in result_tags:
            search_result = SearchResult()

            search_result.title = result_tag.find('h2', {'class': 'search-results-row-game-title'}).text
            tmp_price = result_tag.find('div', {'class': 'search-results-row-price'}).text.strip().replace(',', '.')

            search_result.price = float(tmp_price[0:-1])
            search_result.symbol = tmp_price[-1]

            search_result.href = result_tag.find('a', {'class': 'search-results-row-link'})['href']

            search_results.append(search_result)

        return search_results


if __name__ == '__main__':
    scraper = GoclecdScraper()

    """
    results = scraper.search('grounded')

    for result in results:
        print(result)
    """

    offers = scraper.get_offers('https://www.goclecd.fr/acheter-grounded-cle-cd-comparateur-prix')

    for offer in offers:
        print(offer)