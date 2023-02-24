from base64 import b64encode
from os import getenv

import requests
from dotenv import load_dotenv
from ebaysdk.finding import Connection as Finding

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


def search(keywords: str, categoryId: int = None, sortOrder: str = None, token: str = None):
	if not token:
		token = get_token()

	api = Finding(siteid=getenv('siteid'),
	              appid=getenv('appid'),
	              token=token,
	              config_file=None,
	              proxy_host=proxy_host,
	              proxy_port=proxy_port)

	entries_per_page = 100

	num_pages = 1

	# Loop through the specified number of pages and collect the results
	items = []
	for page_number in range(1, num_pages + 1):
		pagination_input = {'entriesPerPage': entries_per_page, 'pageNumber': page_number}
		params = {'paginationInput': pagination_input, }
		params['keywords'] = keywords
		if categoryId:
			params['category_id'] = categoryId
		if sortOrder:
			params['sortOrder'] = sortOrder

		response = api.execute('findItemsAdvanced', params)
		items += response.reply.searchResult.item

	return items
