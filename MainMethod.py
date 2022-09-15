run = 0
login(1)
money_to_play = 20.0
secs_between_points = 10
my_program_profile = [["Money Alloted to Program",money_to_play],["Amount of Crypto",[get_crypto()]],["Amount of Stock",[]]]
my_crypto = get_number_crypto()
print(MyRobhinhood2.get_crypto_info("DOGE"))
percent_changes = RobinhoodFormulas.check_percentages()
print(percent_changes)


#sell_crypto_quantity("DOGE",my_crypto[1]) - Sells all DOGE currently owned


while run == 1:
    RobinhoodFormulas.store_next_dataPoint(get_crypto_info("DOGE"))
    print(RobinhoodFormulas.get_dataPoints())
    print(RobinhoodFormulas.change_in_percentage_halfhr())
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
