import requests
import json
import pprint
import asyncio

"""a Kraken orderbook data collector"""
class OrderBookCollector_Kraken:
    """store the requested data"""
    data = {}

    def request_bid_or_ask(self, pair, action):
        pair = pair.lower()
        action = self.transform_action(action)

        if self.data:
            return self.data[action]
        elif not self.data:
            return self.request(pair)[action]
        else:
            print('error: data in orderbook class not properly populated')

    def request(self, pair):

        parameters = {"pair": pair, "count": 60}
        response = json.loads(requests.get("https://api.kraken.com/0/public/Depth", params=parameters).text)

        if response['error']:
            print('error: ', response.error)

        self.data = next(iter(response['result'].values()))

        return self.data

    def transform_action(self, action):
        return action + "s"


class OrderBookCollector_Exmo:
    """store the requested data"""
    data = {}

    def request_bid_or_ask(self, pair, action):
        pair = self.transform_pair(pair)

        if self.data:
            return self.data[action]
        elif not self.data:
            return self.request(pair)[action]
        else:
            print('error: data in orderbook class not properly populated')

    def request(self, pair):
        """a Exmo orderbook data collector"""

        parameters = {"pair": pair, "limit": 60}
        response = json.loads(requests.get("https://api.exmo.com/v1/order_book", params=parameters).text)

        self.data = response[pair]

        return self.data

    def transform_pair(self, pair):
        result = ''

        if (len(pair) == 6):
            result = pair[0:3].upper() + "_" + pair[3:6].upper()
        elif (len(pair) == 7):
            result = pair[0:4].upper() + "_" + pair[4:7].upper()
        elif (len(pair) == 8):
            result = pair[0:5].upper() + "_" + pair[5:8].upper()
        else:
            print("pair doesn't exist")

        return result

# d1 = DataCollector_Kraken()
# pprint.pprint(d1.request("adaeth", "bid"))

# d2 = DataCollector_Exmo()
# d2.request("adaeth", "bid")
