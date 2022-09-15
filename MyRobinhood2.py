import config
import json
import robin_stocks as rh
import datetime as dt
import time
import RobinhoodFormulas
import TextFileEditor

#Global Variables to use
stocks = []
crypto = []
money_to_play = 20.0
actions_to_take = []


def login(days):
    '''Logs in to robinbood using the user and pass'''
                                #from the config file
    time_logged_in = 60*60*24*days      #day intake is actually seconds, so this
                                        #converts to days


    #The meat and the potatoes! - Actually logs into Robinhood
    rh.robinhood.authentication.login(username = config.username,
                            password = config.password,
                            expiresIn = time_logged_in,
                            scope = 'internal',
                            by_sms = True,
                            store_session = True)


def logout():
    '''Logs out of Robinhood'''
    rh.robinhood.authentication.logout()

def get_stocks():
    '''Self made stock tracker. You need to type in what stocks are owned'''
    stocks = list()             #makes a list of the currently owned stock
    #stocks.append("BCH")       adds whatever stocks currently owned
    return stocks



def get_crypto():
    '''Makes an array of all crypto planning to work with - update as necessary'''
    cryptos = list()
    cryptos.append("DOGE")
    return cryptos
crypto = get_crypto()           #sets the global variable equal to cryptos



def open_market():
    '''Determines if the markets are currently open'''
    market = False
    time_now = dt.datetime.now().time() #gets the current time

    market_open = dt.time(9,30,0)       #sets the market opening time (9:30)
    market_close = dt.time(15,59,0)     #sets the market closing time (4:00)

    if time_now > market_open and market_close > time_now: #Checks if the market is open
        market = True
    else:
        print('### Market is closed') 

    return market

def open_crypto():
    '''Determines if it's the time I want to trade crypto'''
    market = False
    current_time = dt.datetime.now().time() #gets the current time

    crypto_trade_start = dt.time(22,30,0)       #sets the time to 10:00pm
    crypto_trade_end = dt.time(7,0,0)           #sets the time to 7:00am
    if current_time > crypto_trade_start or current_time < crypto_trade_end: #Checks if the market is open
        market = True
    else:
        print('Not Trading Now') 



def get_important_vals(array):
    '''Gets the values that I have deemed important
    aka -bid price, mark price, low price, and open price'''
    new_array = []
    new_array.append(array[1])
    new_array.append(array[2])
    new_array.append(array[3])
    new_array.append(array[4])
    new_array.append(array[5])
    return new_array


def buy_crypto_price(symbol,quantity):
    rh.robinhood.orders.order_buy_crypto_by_price(symbol,quantity)
    array = get_crypto_info(symbol)
    TextFileEditor.write("\n" + symbol + " Crypto was bought (" + str(quantity) + ") at " + str(dt.datetime.now().time()) + " for " + str(array[0][1] + " per stock"))
    print("Purchases Successfully")

def sell_crypto_price(symbol,quantity):
    rh.robinhood.orders.order_sell_crypto_by_price(symbol,quantity)
    print("Sold Successfully")

def buy_crypto_quantity(symbol,quantity):
    rh.robinhood.orders.order_buy_crypto_by_quantity(symbol,quantity)
    print("Purchases Successfully")

def sell_crypto_quantity(symbol,quantity):
    '''Sells (quantity) of (symbol) crypto'''
    rh.robinhood.orders.order_sell_crypto_by_quantity(symbol,quantity)
    TextFileEditor.write("\n" + symbol + " Crypto was sold (" + str(quantity) + ") at " + str(dt.datetime.now().time()))
    print("Sold Successfully")
    
def get_account_info():
    '''Gets all needed account info'''
    initial_array = list(dict.items(rh.robinhood.account.load_phoenix_account()))
    important_vals = [[],[]]

    important_vals[0].append("Account Buying Power")
    testing = list(dict.items(initial_array[0][1]))
    money = float(testing[2][1])
    important_vals[0].append(money)

    important_vals[1].append("Crypto Buying Power")
    important_vals[1].append(float(list(dict.items(initial_array[8][1]))[2][1]))
    
    return important_vals


def reformat_crypto_info(array):
    '''Makes the info from getting important values easier for me to read and the program to interpret'''
    new_array = [[],[],[],[]]
    new_array[0].append("Bid Price")
    new_array[0].append(float(array[0][1]))
    new_array[1].append("Mark Price")
    new_array[1].append(float(array[1][1]))
    new_array[2].append("Highest Price Today")
    new_array[2].append(float(array[2][1]))
    new_array[3].append("Openning Price Today")
    new_array[3].append(float(array[3][1]))
    return new_array
    
def get_crypto_info(symbl):
    '''Gets crypto data and turns it into an array'''
    array = get_important_vals(list(dict.items(rh.robinhood.crypto.get_crypto_quote(symbl))))
    array = reformat_crypto_info(array)
    array.append(str(dt.datetime.now().time()))
    array.append([])
    time = array[4]
    array[5].append(int(time[:2]))
    array[5].append(int(time[3:5]))
    array[5].append(float(time[6:]))
    return(array)

def get_number_crypto():
    '''Returns the number of crypto that is currently owned. At the moment, it only
    returns the number of DOGE crypto owned. Will fix in the future'''
    array = rh.robinhood.crypto.get_crypto_positions()
    array = list(dict.items(array[1]))
    array = array[5]
    new_array = ["Amount of DOGE",float(array[1])]
    return new_array

def sell_crypto_limit(symbol):
    '''Sells all of the crypto (symbl) that is currently owned'''
    rh.robinhood.orders.order_sell_crypto_limit(symbol)
    print("Sold Successfully")

#def interpret_actions_to_take(actions):
    

    

run = 1
login(1)
secs_between_points = 10
my_program_profile = [["Money Allowed to Program",money_to_play],["Amount of Crypto",[get_crypto()]],["Amount of Stock",[]]]
my_crypto = get_number_crypto()

while run == 0: #compares prices
    RobinhoodFormulas.store_next_dataPoint(get_crypto_info("DOGE"))
    current_percentages_doge = RobinhoodFormulas.check_percentages()
    actions_to_take = RobinhoodFormulas.check_buy_or_sell(current_percentages_doge,money_to_play)
    getPoints = RobinhoodFormulas.get_dataPoints()
    current_percentages_doge = RobinhoodFormulas.check_percentages()  
    print(getPoints)
    print(current_percentages_doge)
    print(actions_to_take,"\n")
    #if actions_to_take
    time.sleep(secs_between_points)
    


#sell_crypto_quantity("DOGE",my_crypto[1]) - Sells all DOGE currently owned


while run == 1:     #collects data
    RobinhoodFormulas.store_next_dataPoint(get_crypto_info("DOGE"))
    #print(RobinhoodFormulas.get_dataPoints())
    #print(RobinhoodFormulas.change_in_percentage_halfhr())
    getPoints = RobinhoodFormulas.get_dataPoints()
    current_percentages_doge = RobinhoodFormulas.check_percentages()  
    print(current_percentages_doge)
    print(getPoints)
    print(" ")
    time.sleep(secs_between_points)
    
    
#myFormulas allows the use of any formulas for comparing data points
    
#This code is specifically for STOCK and NOT CRYPTO
          #Currently does not run code
if run == 2:      #Main Mehod of the code
    login(1)
    stocks = get_stocks()
    print("Stocks: ",stocks)
    
    while open_market():
        prices = rh.robinhood.stocks.get_latest_price(stocks)
        
        for i,stock in enumerate(stocks):
            price = float(prices[i])
            print('{} = ${}'.format(stock,price))
            
        time.sleep(30) 
        
        
    logout()
