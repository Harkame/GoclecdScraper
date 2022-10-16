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


class Offer():
    def __init__(self):
        self.title = None
        self.merchant_name = None
        self.price = 0.0
        self.currency = None
        self.coupon = None
        self.price_without_coupon = 0.0
        self.edition = None
        self.review_count = 0
        self.href = None

    def __str__(self):
        str = ''

        str += f'Title : {self.title}'
        str += os.linesep

        str += f'Merchant name : {self.merchant_name}'
        str += os.linesep

        str += f'Price : {self.price} {self.currency}'
        str += os.linesep

        str += f'Price without coupon : {self.price_without_coupon} {self.currency}'
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

def currency_to_symbol(currency):
    symbol = None

    if currency == 'eur':
        symbol = '€'

    return symbol

class GoclecdScraper():
    def __init__(self):
        pass

    def get_offers(self, url, currency='eur'):
        content = requests.get(url).content

        page = BeautifulSoup(content, 'lxml')

        offers_table = page.find('div', {'class': 'offers-table x-offers'})

        product_id = page.find('a', {'class': 'aks-follow-btn aks-follow-btn-score aks-follow-btn-score-green game-aside-button jc-center col-4'})['data-product-id']

        result = requests.get(f'https://www.goclecd.fr/wp-admin/admin-ajax.php?action=get_offers&product={product_id}&currency={currency}&region=&edition=&moreq=&use_beta_offers_display=1').json()

        offers = []

        #print(offers_json['merchants'])
        for offer_json in result['offers']:
            print(offer_json)

            offer = Offer()

            merchant_json = result['merchants'][offer_json['merchant']]
            print(merchant_json)

            offer.currency = currency_to_symbol(currency)
            offer.price = float(offer_json['price'][currency]['price'])
            offer.price_without_coupon = float(offer_json['price'][currency]['priceWithoutCoupon'])

            offers.append(offer)

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
        pass
        #print(offer)