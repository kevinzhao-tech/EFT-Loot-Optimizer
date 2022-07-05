from pytarkovdata import send_query

class Item:
    # TODO Peacekeeper prices are returned as USD so comparison is not corret, need to be fixed
    """
    Creates a new Item object from an uid
    """
    def __init__(self, uid):
        new_query = '''
            {{
                item(id: "{}") {{
                    name

                    sellFor {{
                        vendor {{name}}
                        priceRUB
                    }}

                    width
                    height

                    usedInTasks {{
                        id
                        name
                        trader {{name}}
                    }}
                }}
            }}
            '''
        query_result = send_query(new_query.format(uid))

        self.uid = uid
        self.name = query_result['data']['item']['name']

        self.prices = {}
        for key in query_result['data']['item']['sellFor']:
            vendor = key['vendor']['name']
            price = key['priceRUB']
            self.prices[vendor] = price

        self.task_usages = []
        for task in query_result['data']['item']['usedInTasks']:
            self.task_usages.append((task['id'], task['name'], task['trader']['name']))

        self.slots = query_result['data']['item']['width'] * query_result['data']['item']['height']

    def get_optimal_trader(self, ignore_flea=False):
        best_price = 0
        best_trader = None
        for trader in self.prices:
            ignore = ignore_flea and (trader == 'Flea Market')
            if self.prices[trader] > best_price and not ignore:
                best_trader = trader
                best_price = self.prices[trader]

        return best_trader, best_price


if __name__ == '__main__':
    test = Item('5734779624597737e04bf329')
    print(test.get_optimal_trader(True))
