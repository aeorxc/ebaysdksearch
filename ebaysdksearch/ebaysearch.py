from base64 import b64encode
from os import getenv

import requests
from dotenv import load_dotenv
from ebaysdk.finding import Connection as Finding
from cachetools import cached, TTLCache
import logging

load_dotenv()

tokenurl = 'https://api.ebay.com/identity/v1/oauth2/token'

proxies = {}
if getenv('http'):
    proxies = {
        'http': getenv('http'),
        'https': getenv('https')
    }

proxy_host, proxy_port = None, None
if getenv('http'):
    proxy_host = getenv('http').replace('http://', '').split(':')[0]
    proxy_port = getenv('http').replace('http://', '').split(':')[1]

cache = TTLCache(maxsize=100, ttl=300)  # create a TTL cache with a maximum size of 100 items and a TTL of 60 seconds


@cached(cache)
def get_token():
    """
    Require the token to ebay
    """
    authHeaderData = getenv("appid") + ':' + getenv("app_secret")
    encodedAuthHeader = b64encode(str.encode(authHeaderData))
    encodedAuthHeader = str(encodedAuthHeader)[2:len(str(encodedAuthHeader)) - 1]
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + encodedAuthHeader
    })

    data = {
        'grant_type': 'client_credentials',
        'scope': 'https://api.ebay.com/oauth/api_scope'
    }

    response = session.post(tokenurl, data=data, proxies=proxies).json()
    return response["access_token"]


def search(params: dict = {}, keywords: str = None, num_pages: int = 1, categoryId: int = None, sortOrder: str = None,
           token: str = None):
    if not token:
        token = get_token()

    api = Finding(siteid=getenv('siteid'),
                  appid=getenv('appid'),
                  token=token,
                  config_file=None,
                  proxy_host=proxy_host,
                  proxy_port=proxy_port)

    entries_per_page = 100

    # Loop through the specified number of pages and collect the results
    items = []
    for page_number in range(1, num_pages + 1):
        pagination_input = {'entriesPerPage': entries_per_page, 'pageNumber': page_number}
        params = {**params, 'paginationInput': pagination_input, }

        if keywords:
            params['keywords'] = keywords
        if categoryId:
            params['categoryId'] = str(categoryId) if isinstance(categoryId, int) else categoryId
        if sortOrder:
            params['sortOrder'] = sortOrder

        logging.info(f'search params: {params}')

        if 'keywords' not in params and 'categoryId' in params:
            response = api.execute('findItemsByCategory', params)
        else:
            response = api.execute('findItemsAdvanced', params)

        if response.reply.ack != 'Success':
            raise Exception('eBay API returned an error: ' + str(response.reply.errorMessage.error.message))
        logging.info(f'ebay url: {response.reply.itemSearchURL}')
    items += response.reply.searchResult.item

    return items


def search_auction(params: dict = {}, keywords: str = None, num_pages: int = 1, categoryId: int = None,
                   token: str = None):
    if 'itemFilter' not in params:
        params['itemFilter'] = []

    params['itemFilter'].append({'name': 'ListingType', 'value': ['Auction']})
    params['itemFilter'].append({'name': 'HideDuplicateItems', 'value ': 'true'})
    return search(params=params, keywords=keywords, num_pages=num_pages, categoryId=categoryId, token=token,
                  sortOrder='EndTimeSoonest')


def search_bin(params: dict = {}, keywords: str = None, num_pages: int = 1, categoryId: int = None,
               token: str = None):
    if 'itemFilter' not in params:
        params['itemFilter'] = []

    params['itemFilter'].append({'name': 'ListingType', 'value': ['AuctionWithBIN', 'FixedPrice']})
    params['itemFilter'].append({'name': 'HideDuplicateItems', 'value ': 'true'})
    return search(params=params, keywords=keywords, num_pages=num_pages, categoryId=categoryId, token=token,
                  sortOrder='StartTimeNewest')
