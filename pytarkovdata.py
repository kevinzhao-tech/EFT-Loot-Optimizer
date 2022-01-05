import requests
from Item import Item
from pykson import Pykson, JsonObject, IntegerField, StringField, ObjectListField

"""
This is a simple wrapper for the tarkov-tools API.
"""


def send_query(query) -> str:
    """
    sends a request to the API and returns the response as a json object

    Args:
        query: the query to send to the API
    Returns:
        the response as a json object
    """
    response = requests.post('https://tarkov-tools.com/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed - Code: {}".format(response.status_code))


def get_optimal_trade(uid):
    """
    gets the optimal trader given an item UID

    Args:
        uid: the UID of the item

    Returns:
        the optimal trader for the item
    """
    new_query = '''
    {{
        item(id: "{}") {{
            name
            traderPrices {{
              trader {{name}}
              price
            }}
        }}
    }}
    '''
    query_result = send_query(new_query.format(uid))

    # get the name of the trader with the lowest price
    highest_price = 0
    highest_trader = None
    for price in query_result['data']['item']['traderPrices']:
        if price['price'] > highest_price:
            highest_price = price['price']
            highest_trader = price['trader']['name']

    return highest_trader, highest_price


def get_optimal_trader_by_name(item_name):
    """
    gets the optimal trader for an item given its name

    Args:
        item_name: the name of the item

    Returns:
        the optimal trader for the item

    Raises:
        Exception: if the item does not exist
    """
    uid = get_uid(item_name)
    return get_optimal_trade(uid)


def get_uid(item_name):
    """
    gets the UID of an item given its name
    Args:
        item_name: the name of the item

    Returns:
        the UID of the item, None if the item does not exist

    Raises:
        Exception: if the item does not exist
    """
    new_query = '''
    {{
        itemsByName(name: "{}") {{
            id
        }}
    }}
    '''
    query_result = send_query(new_query.format(item_name))

    # check if query_result['data']['itemsByName'] is empty
    if not query_result['data']['itemsByName']:
        raise Exception("Item does not exist")
    return query_result['data']['itemsByName'][0]['id']


def get_list_of_UIDs(item_name):
    """
    gets the UIDs of all items with the given name

    Args:
        item_name: the name of the item

    Returns:
        a list of UIDs of all items with the given name, None if the item does not exist
    """
    new_query = '''
    {{
        itemsByName(name: "{}") {{
            name
            id
        }}
    }}
    '''
    # create a dictionary of names and UIDs
    query_result = send_query(new_query.format(item_name))

    # check if query_result['data']['itemsByName'] is empty
    if not query_result['data']['itemsByName']:
        raise Exception("Item does not exist")
    uid_dict = {}
    for item in query_result['data']['itemsByName']:
        uid_dict[item['name']] = item['id']
    return uid_dict


if __name__ == '__main__':
    """
    This is a test of the API wrapper.
    Given an item name, it will print the optimal trader and price.
    """
    name = input("Enter Item Name: ")
    print(get_optimal_trader_by_name(name))
    while True:
        name = input("Enter Item Name: ")
        print(get_optimal_trader_by_name(name))
