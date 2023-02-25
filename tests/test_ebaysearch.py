from ebaysdksearch import ebaysearch
import pytest


def test_get_token():
    res = ebaysearch.get_token()
    assert res is not None


@pytest.mark.parametrize(
    "params, keywords, categoryId, sortOrder",
    [
        ({'itemFilter': [{'name': 'LocatedIn', 'value ': 'GB'},
                         {'name': 'HideDuplicateItems', 'value ': 'true'},
                         {'name': 'MinPrice', 'value': '100', 'paramName': 'Currency', 'paramValue': 'GBP'},
                         {'name': 'ExcludeSeller', 'value': ['currys', 'argos', ]},
                         {'name': 'ListingType', 'value': ['AuctionWithBIN', 'FixedPrice']},
                         {'name': 'Condition',
                          'value ': ['1000', '1500', '1750', '2000', '2500', '3000', '4000', '5000', '6000']}],
          }, 'phone', 9355, 'StartTimeNewest'),

    ]
)
def test_search(params, keywords, categoryId, sortOrder):
    res = ebaysearch.search(params=params, keywords=keywords, categoryId=categoryId, sortOrder=sortOrder)
    assert len(res) > 0


def test_search_auction():
    params = {'itemFilter': [{'name': 'LocatedIn', 'value ': 'GB'},
                             {'name': 'MinPrice', 'value': '100', 'paramName': 'Currency', 'paramValue': 'GBP'},
                             ]
              }
    res = ebaysearch.search_auction(params=params, keywords='phone', categoryId=9355)
    assert len(res) > 0


def test_search_bin():
    params = {'itemFilter': [{'name': 'LocatedIn', 'value ': 'GB'},
                             {'name': 'MinPrice', 'value': '100', 'paramName': 'Currency', 'paramValue': 'GBP'},
                             ]
              }
    res = ebaysearch.search_bin(params=params, keywords='phone', categoryId=9355)
    assert len(res) > 0
