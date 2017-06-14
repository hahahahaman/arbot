import requests

def getOrders(coin, market):
        url = 'https://tuxexchange.com/api?method=getorders&coin=' + coin + '&market=' + market
        r = requests.get(url)
        return r.json()

def displayJSONOrderSpread(data):
    ask = data['asks'][0][0]
    bid = data['bids'][0][0]
    print("lowest ask:", ask)
    print("highest bid:", bid)
    print("spread: %.5f%%" % ((float(ask)/float(bid) - 1) * 100))

def displayOrderSpread(coin, market):
    print(coin + "-" + market)
    displayJSONOrderSpread(getOrders(coin, market))
    print('')



displayOrderSpread('DCR', 'BTC')
displayOrderSpread('PEPECASH', 'BTC')

