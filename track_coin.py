# import Assing_keys
from binance import Client
from pprint import pprint
from forex_python.converter import CurrencyRates

c = CurrencyRates()
current_inr=c.get_rate('USD', 'INR')
current_euro=c.get_rate('USD','EUR')
current_yen=c.get_rate('USD','JPY')


api_key = "LP87spAIaElsHx8WKfCa2bTb4IZPfWtKRQNIkRWsUDnMKkJA0Cd0nHvahkd6SByk"
api_secreat = "N7SN9lVLiO01DFtZMBnzCC3H0uCVnem7ymaw9IXraWgv71oNByo15DgLyS4pHMhk"

# # client = Client(api_key, api_secreat ,tld='us')

def crypto_calculate(symb,currency="USD"):
    symbol=str(symb)+"busd"
    symbol=symbol.upper()
    currency=currency.upper()
    new_price=""
    # client = Client(api_key, api_secreat )
    client = Client(api_key, api_secreat)
    try:

        data_price = client.get_symbol_ticker(symbol=symbol)
        us_price=float(data_price["price"])
        
        if currency=="USD":
            price= us_price
            try:
                price=str(price)
                split_price=price.split('.')
                lenght=len(split_price[0])+4
                for i in range(lenght):
                    new_price=new_price+str(price[i])
                return new_price
                # print(us_price)
            except:
                return price
        elif currency=="INR":
            price= us_price*current_inr
            price=str(price)
            split_price=price.split('.')
            lenght=len(split_price[0])+4
            for i in range(lenght):
                new_price=new_price+str(price[i])
            return new_price
            # print(new_price)

        elif currency=="EURO":
            price= us_price*current_euro
            price=str(price)
            split_price=price.split('.')
            lenght=len(split_price[0])+4
            for i in range(lenght):
                new_price=new_price+str(price[i])
            return new_price
            # print(new_price)
        elif currency=="YEN":
            price=us_price*current_yen
            price=str(price)
            split_price=price.split('.')
            lenght=len(split_price[0])+4
            for i in range(lenght):
                new_price=new_price+str(price[i])
            return new_price
            # print(new_price)
        
    except:
        print("An exception occurred")
        # return "error"

    # print(btc_price["price"])
    
def crypto_calculate2(symb):
    symbol=symb.upper()
    # client = Client(api_key, api_secreat )
    client = Client(api_key, api_secreat)
    try:

        crypto_price = client.get_symbol_ticker(symbol=symbol)
        us_price=float(crypto_price["price"])
        # rupees=rs*73.16
        print(crypto_price)
        # return us_price
        
    except:
    # print("An exception occurred")
        return "error"


def inr_calculate():
    symbol="BTCBUSD"
    symbol=symbol.upper()
    print("hello")

    # client = Client(api_key, api_secreat )
    client = Client(api_key, api_secreat)
    try:

        btc_price = client.get_symbol_ticker(symbol=symbol)
        rs=float(btc_price["price"])
        rupees=rs*inr 
        print(rs)
        print(rupees)
        # return rupees
        
    except():
        # print("error")
        return "error"

# price=crypto_calculate("btc")
# print(price)