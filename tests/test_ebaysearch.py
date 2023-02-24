from ebaysdksearch import ebaysearch


def test_get_token():
	res = ebaysearch.get_token()
	assert res is not None


def test_search():
	res = ebaysearch.search(keywords='iphone', categoryId='9355', sortOrder='StartTimeNewest', )
	assert len(res) > 0
