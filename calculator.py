import requests
import json
import pprint
import data_collector
import time


# TODO
def find_all_pairs(ex1, ex2):
    pass


class calculator:

    # d1 = data_collector.DataCollector_Kraken()
    # d2 = data_collector.DataCollector_Exmo()


    values = [] # to store pairs values in USD to easily calculate lot

    """calculates arbitrage between any two exchanges"""
    def calculate_all(self, trade_amount):
        commonpairs = ["ADAUSD", "ADAETH", "DASHUSD", "EOSUSD", "EOSEUR", "ETHUSD", "ETHEUR", "XLMUSD", "XRPUSD", "XRPEUR"]
        for pair in commonpairs:
            self.calculate(pair, trade_amount)

    def calculate(self, pair, trade_amount):

        # initiate the data collectors
        print(pair)
        d1 = data_collector.OrderBookCollector_Kraken()
        d2 = data_collector.OrderBookCollector_Exmo()


        # get data going from exchange 1 to exchange 2
        d1asks = d1.request_bid_or_ask(pair, "ask")
        d1askprice = self.calculate_rate(d1asks, pair, trade_amount)

        d2bids = d2.request_bid_or_ask(pair, "bid")
        d2bidprice = self.calculate_rate(d2bids, pair, trade_amount)

        forward_arbitrage = (d2bidprice - d1askprice) / d1askprice # arbitrage buying from ex1 and selling on ex2
        forward_arbitrage = forward_arbitrage * 100


        # get data going from exchange 2 to exchange 1
        d2asks = d2.request_bid_or_ask(pair, "ask")
        d2askprice = self.calculate_rate(d2asks, pair, trade_amount)

        d1bids = d1.request_bid_or_ask(pair, "bid")
        d1bidprice = self.calculate_rate(d1bids, pair, trade_amount)

        backward_arbitrage = (d1bidprice - d2askprice) / d2askprice # arbitrage buying from ex2 and selling on ex1
        backward_arbitrage = backward_arbitrage * 100

        """
        for this to work we want to forward arbitrage to be high and backward
        arbitrage to be low
        """

        print(forward_arbitrage, ", ", backward_arbitrage)

    def calculate_rate(self, list, pair, trade_amount):

        threshold = self.find_lot(pair, trade_amount) # returns the quantity needed

        total_sum = 0.0
        total_quantity = 0.0

        for item in list:
            price = float(item[0])
            quantity = float(item[1])
            total_quantity += quantity
            total_sum += price * quantity
            if total_quantity > threshold:
                break
        if total_quantity < threshold:
            print("requested order book orders too few, threshold not reached")
        average_price = total_sum / total_quantity
        return average_price

    # returns the quantity given a trade's USD amount
    def find_lot(self, pair, trade_amount):
        result = 0
        buying_currency = pair[len(pair) - 3 : len(pair)]

        if buying_currency == "usd" or buying_currency == "USD":
            parameters = {"pair": pair}
            response = json.loads(requests.get("https://api.kraken.com/0/public/Ticker", params=parameters).text)
            result = float(next(iter(response['result'].values()))['c'][0])
        else:


            pair = pair.replace(buying_currency, 'USD')
            parameters = {"pair": pair}
            response = json.loads(requests.get("https://api.kraken.com/0/public/Ticker", params=parameters).text)
            result = float(next(iter(response['result'].values()))['c'][0])
        return trade_amount / result

            # pprint.pprint(response)



start_time = time.time()

c1 = calculator()
c1.calculate_all(300)
# c1.find_lot("adausd", 10000)
print("--- %s seconds ---" % (time.time() - start_time))
