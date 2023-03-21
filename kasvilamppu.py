from PyP100 import PyP100
import requests
import schedule
import time

p100 = PyP100.P100("192.168.XXX.XXX", "example@email.com", "password123!")  # Creates a P100 plug object
p100.handshake()  # Creates the cookies required for further methods
p100.login()  # Sends credentials to the plug and creates AES Key and IV for further methods

# get hourly electricity price from spot-hinta.fi api as json
# and after that get just the price from the json
def get_hour_price():
    api_url = "http://api.spot-hinta.fi/JustNow"
    response = requests.get(api_url).json()
    hour_price = response['PriceWithTax']
    return hour_price

# turn the light on if the price is under 0.05e
# and off it is more expensive than 0.05e
def if_cheap_light():
    print(time.ctime())
    print("current price: ",get_hour_price())
    if get_hour_price() < 0.0500:
        p100.turnOn()
    else:
        p100.turnOff()


# run if_cheap_light function every hour
def main():
    schedule.every().hour.at(":02").do(if_cheap_light)
    while True:
        schedule.run_pending()
        time.sleep(1)
        #print(schedule.idle_seconds())
        
main()
