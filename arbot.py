import requests
import sched, time

waitTime = 2

def getOrders(coin, market):
        url = 'https://tuxexchange.com/api?method=getorders&coin=' + coin + '&market=' + market
        r = requests.get(url)
        return r.json()

def displayJSONOrderSpread(data):
    ask = data['asks'][0][0]
    ask_volume = data['asks'][0][1]
    bid = data['bids'][0][0]
    bid_volume = data['bids'][0][1]
    print("lowest ask:", ask, ", volume:", ask_volume)
    print("highest bid:", bid, ", volume:", bid_volume)
    print("spread: %.5f%%" % ((float(ask)/float(bid) - 1) * 100))

def displayOrderSpread(coin, market):
    print(coin + "-" + market)
    displayJSONOrderSpread(getOrders(coin, market))
    print('')


s = sched.scheduler(time.time, time.sleep)
def loop(sc):

    print("\n\nTime:", time.time())
    print("Getting data...\n")

    displayOrderSpread('DCR', 'BTC')
    displayOrderSpread('PEPECASH', 'BTC')

    s.enter(waitTime,1, loop, (sc,))

s.enter(waitTime,1, loop, (s,))
s.run()

# bittrex poloniex ETH spread
