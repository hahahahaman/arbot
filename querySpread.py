import requests
import sched, time
from datetime import datetime

waitTime = 2

def spread(ask, bid):
        return (ask/bid)-1

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

def displayPoloniexBittrexSpead(base, counter):
        poloURL = "https://poloniex.com/public?command=returnOrderBook&currencyPair=" + base.upper() + "_" + counter.upper() + "&depth=2"
        # bitURL = "https://bittrex.com/api/v1.1/public/getorderbook?market=" + base.upper() + "-" + counter.upper() + "&type=both&depth=2"
        bitURL = "https://bittrex.com/api/v1.1/public/getticker?market=" + base.upper() + "-" + counter.upper()
        poloData = requests.get(poloURL).json()
        bitData = requests.get(bitURL).json()['result']


        poloHiBid = float(poloData['bids'][0][0])
        poloLowAsk = float(poloData['asks'][0][0])

        bitHiBid = float(bitData['Bid'])
        bitLowAsk = float(bitData['Ask'])
        bpSpread = spread(bitLowAsk, poloHiBid) * 100
        pbSpread = spread(poloLowAsk, bitHiBid) * 100

        if(abs(bpSpread) >= 5 or abs(pbSpread) >= 5):
                with open("query.log", 'a') as f:
                        f.write(str(datetime.now()) + '\n')
                        f.write(counter, '-', base)
                        f.write("Poloniex Bid:", poloHiBid)
                        f.write("Poloniex Ask:", poloLowAsk)
                        f.write("Bittrex Bid:", bitHiBid)
                        f.write("Bittrex Ask:", bitLowAsk, "\n")
                        f.write("Bittrex-Poloniex Spread:", bpSpread, "%")
                        f.write("Poloniex-Bittrex Spread:", pbSpread, "%")

        print(counter, '-', base)
        print("Poloniex Bid:", poloHiBid)
        print("Poloniex Ask:", poloLowAsk)
        print("Bittrex Bid:", bitHiBid)
        print("Bittrex Ask:", bitLowAsk, "\n")
        print("Bittrex-Poloniex Spread:", bpSpread, "%")
        print("Poloniex-Bittrex Spread:", pbSpread, "%")

        # print("Poloniex:")
        # print(poloData)
        # print("")
        # print("Bittrex:")
        # print(bitData)

s = sched.scheduler(time.time, time.sleep)
def loop(sc):

    print("\n\nTime:", str(datetime.now()))
    print("Getting data...\n")

    # displayOrderSpread('DCR', 'BTC')
    # displayOrderSpread('PEPECASH', 'BTC')
    displayPoloniexBittrexSpead('USDT', 'ETH')

    s.enter(waitTime,1, loop, (sc,))

s.enter(waitTime,1, loop, (s,))
s.run()

# bittrex poloniex ETH spread

