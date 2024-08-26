# # import time
# # import os
# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.common.keys import Keys

# # def download_csv(chrome_driver_path, login_url, username, password):
# #     # Initialize Chrome WebDriver
# #     service = Service(chrome_driver_path)
# #     options = webdriver.ChromeOptions()
# #     driver = webdriver.Chrome(service=service, options=options)
    
# #     try:
# #         # Open the login URL
# #         driver.get(login_url)
# #         time.sleep(2)
        
# #         # Locate the username and password fields and enter the credentials
# #         username_field = driver.find_element(By.NAME, "email")
# #         password_field = driver.find_element(By.NAME, "password")
# #         username_field.send_keys(username)
# #         password_field.send_keys(password)
# #         password_field.send_keys(Keys.RETURN)
# #         time.sleep(2)
        
# #         # Click on the button to navigate to the correct page
# #         button1 = driver.find_element(By.XPATH, "//*[@class='table table-striped']//tr[8]//a")
# #         button1.click()
# #         time.sleep(2)
        
# #         # Click on the download button with the new XPath
# #         download_button = driver.find_element(By.XPATH, '//*[@id="backtest-container"]/div[2]/a')
# #         download_button.click()
# #         time.sleep(5)  # Wait for the download to complete; adjust if needed

# #     except Exception as e:
# #         print(f"An error occurred: {e}")
    
# #     finally:
# #         driver.quit()

# # # Example usage
# # chrome_driver_path = r'C:\Users\omkar\AppData\Local\Google\Chrome\User Data\Default\chromedriver-win64\chromedriver.exe'
# # login_url = "https://chartink.com/login"
# # username = "akashkharade.760@gmail.com"
# # password = "7030232281"

# # # Call the function
# # download_csv(chrome_driver_path, login_url, username, password)

# import csv
# from datetime import datetime as dt_datetime, timedelta
# import time
# import threading
# import logging
# import pandas as pd
# from NorenRestApiPy.NorenApi import NorenApi
# import pyotp
 
# class ShoonyaApiPy(NorenApi):
#     def __init__(self):
#         super().__init__(host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')
 
# # Configuration Constants
# USER = 'FA74468'
# PWD = 'GURU222kore$'
# TOKEN = 'XT2L66VT73Q22P33BNCHKN6WA2Q37KK6'
# VC = 'FA74468_U'
# APP_KEY = 'c98e82a190da8181c80fb94cf0a31144'
# IMEI = 'abc1234'
# CSV_FILE_PATH = "C:\\Users\\omkar\\Downloads\\Backtest BB Blast_Omk, Technical Analysis Scanner.csv"
# REMOVE_STOCKS = ['M&M-EQ', 'M&MFIN-EQ', 'J&KBANK-EQ']
# processed_stocks = set()
 
# # Logging Configuration
# logging.basicConfig(
#     filename='D:\\AA_trading_Algos\\modified_ALgo\\trading_log.txt',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     filemode='w'
# )
 
# # Initialize API
# api = ShoonyaApiPy()
# factor2 = pyotp.TOTP(TOKEN).now()
# api.login(userid=USER, password=PWD, twoFA=factor2, vendor_code=VC, api_secret=APP_KEY, imei=IMEI)
 
# def parse_datetime(date_str):
#     formats = ["%d-%m-%Y %I:%M %p", "%d-%m-%Y %H:%M"]
#     for fmt in formats:
#         try:
#             return dt_datetime.strptime(date_str, fmt)
#         except ValueError:
#             continue
#     raise ValueError(f"Date parsing error: time data '{date_str}' does not match any of the known formats.")
 
# def extract_stock_list_from_csv(csv_file_path, target_datetime_str):
#     stock_list = []
#     try:
#         target_datetime = parse_datetime(target_datetime_str)
#         target_date = target_datetime.date()
#         target_time = target_datetime.time()
 
#         with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 try:
#                     row_datetime = parse_datetime(row['date'])
#                 except ValueError:
#                     continue
 
#                 if row_datetime.date() == target_date and row_datetime.time() == target_time:
#                     stock_list.append(f"{row['symbol']}-EQ")
#     except Exception as e:
#         logging.error(f"An error occurred while extracting stock list: {e}")
#     return stock_list
 
# def place_orders(target_datetime_str):
#     global stocksList, slArray, tgtArray
 
#     stocksList = extract_stock_list_from_csv(CSV_FILE_PATH, target_datetime_str)
#     stocksList = [symbol for symbol in stocksList if symbol not in REMOVE_STOCKS]
 
#     if len(stocksList) > 3:
#         stocksList = []
#         logging.info("More than 3 stocks found. No orders will be placed.")
#     elif not stocksList:
#         slArray = []
#         tgtArray = []
#         logging.info("No stocks found for the given time. Clearing previous stock lists.")
#     else:
#         slArray = []
#         tgtArray = []
 
#         for symbol in stocksList:
#             try:
#                 quote = api.get_quotes(exchange='NSE', token=symbol)
#                 LTP = float(quote["lp"])
 
#                 stop_loss = round(LTP * 1.0045, 2)
#                 target = round(LTP * 0.992, 2)
#                 Qty_Stock = round(10000 / LTP)
#                 slArray.append(stop_loss)
#                 tgtArray.append(target)
 
#                 logging.info(f"LTP: {LTP}, Stop-Loss: {stop_loss}, Target: {target} for symbol: {symbol}")
 
#                 api.place_order(
#                     buy_or_sell='S', product_type='I', exchange='NSE', tradingsymbol=symbol,
#                     quantity=Qty_Stock, discloseqty=0, price_type='MKT', trigger_price=None,
#                     retention='DAY', remarks='Place_order'
#                 )
#                 logging.info(f"Order placed for symbol: {symbol}")
 
#             except Exception as e:
#                 logging.error(f"Error occurred for symbol {symbol}: {e}")
 
#     logging.info("place_orders function completed.")
 
# def place_buy_orders_based_on_positions():
    
#     positions = api.get_positions()
#     df = pd.DataFrame(positions)

#     df = pd.DataFrame(positions)

#                 # Extract fields and initialize arrays

#     tsym_array = df['tsym'].dropna().tolist() if 'tsym' in df.columns else []

#     rpnl_array = pd.to_numeric(df['rpnl'], errors='coerce').fillna(float('nan')).tolist() if 'rpnl' in df.columns else []

#     daysellqty_array = pd.to_numeric(df['daysellqty'], errors='coerce').fillna(0).astype(int).tolist() if 'daysellqty' in df.columns else []


#     for i in range(len(tsym_array)):
#         stock_name = tsym_array[i]

#         rpnl_value = rpnl_array[i]

#         quantity = daysellqty_array[i]

#         if stock_name in processed_stocks:
#             continue
#         if rpnl_value<=-40 or rpnl_value >=79:
#             ret = api.place_order(buy_or_sell='B', product_type='I',
#                             exchange='NSE', tradingsymbol=stock_name, 
#                             quantity=quantity, discloseqty=0,price_type='MKT',
#                             retention='DAY', remarks='my_order_001')
#             print(stock_name)

#             processed_stocks.add(stock_name)
#             logging.info(f"Buy order placed for {stock_name}. Quantity: {quantity}, PnL: {rpnl_value}")
#         else:

#             logging.error("No positions data found or data is not in the expected format.")
        

 
# def round_down_to_nearest_15_minutes(dt):
#     new_minute = (dt.minute // 15) * 15
#     return dt.replace(minute=new_minute, second=0, microsecond=0)
 
# def get_previous_timestamp():
#     now = dt_datetime.now()
#     previous_time = now - timedelta(minutes=15)
#     rounded_time = round_down_to_nearest_15_minutes(previous_time)
#     return rounded_time.strftime('%d-%m-%Y %I:%M %p')
 
# def schedule_place_orders(start_time, end_time):
#     while dt_datetime.now().time() <= end_time:
#         if dt_datetime.now().time() >= start_time:
#             target_datetime_str = get_previous_timestamp()
#             logging.info(f"Placing orders for {target_datetime_str}")
#             place_orders(target_datetime_str)
#             time.sleep(15 * 60)  # Sleep for 15 minutes
#         else:
#             time.sleep(1)  # Wait until the start time is reached
 
# def schedule_check_positions(start_time, end_time):
#     while dt_datetime.now().time() <= end_time:
#         if dt_datetime.now().time() >= start_time:
#             logging.info("Checking positions and placing orders.")
#             place_buy_orders_based_on_positions()  # Updated function call
#             time.sleep(10)  # Sleep for 10 seconds
#         else:
#             time.sleep(1)  # Wait until the start time is reached
 
# if __name__ == "__main__":
#     # Custom Start and End Times (Adjust these for testing)
#     place_orders_start_time = dt_datetime.strptime("10:15", "%H:%M").time()
#     place_orders_end_time = dt_datetime.strptime("11:45", "%H:%M").time()
 
#     check_positions_start_time = dt_datetime.strptime("10:18", "%H:%M").time()
#     check_positions_end_time = dt_datetime.strptime("15:10", "%H:%M").time()
 
#     # Start place_orders function on a separate thread
#     place_orders_thread = threading.Thread(target=schedule_place_orders, args=(place_orders_start_time, place_orders_end_time))
#     place_orders_thread.start()
 
#     # Start place_buy_orders_based_on_positions function on another thread
#     check_positions_thread = threading.Thread(target=schedule_check_positions, args=(check_positions_start_time, check_positions_end_time))
#     check_positions_thread.start()
 
#     place_orders_thread.join()
#     check_positions_thread.join()











#####################################################################
#########    THIS IS CODE UPDATED WITH GLONAL VARIABLES     #########
#####################################################################
 

import csv
from datetime import datetime as dt_datetime, timedelta
import time
import threading
import logging
import pandas as pd
from NorenRestApiPy.NorenApi import NorenApi
import pyotp

class ShoonyaApiPy(NorenApi):
    def __init__(self):
        super().__init__(host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')

# Configuration Constants
USER = 'FA74468'
PWD = 'GURU222kore$'
TOKEN = 'XT2L66VT73Q22P33BNCHKN6WA2Q37KK6'
VC = 'FA74468_U'
APP_KEY = 'c98e82a190da8181c80fb94cf0a31144'
IMEI = 'abc1234'
CSV_FILE_PATH = "C:\\Users\\omkar\\Downloads\\Backtest BB Blast_Omk, Technical Analysis Scanner.csv"
REMOVE_STOCKS = ['M&M-EQ', 'M&MFIN-EQ', 'J&KBANK-EQ']
processed_stocks = set()

# Logging Configuration
logging.basicConfig(
    filename='D:\\AA_trading_Algos\\modified_ALgo\\trading_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

# Global Variables
stocksList = []
slArray = []
tgtArray = []
stock_names = []
rpnl_values = []
quantities = []

# Initialize API
api = ShoonyaApiPy()
factor2 = pyotp.TOTP(TOKEN).now()
api.login(userid=USER, password=PWD, twoFA=factor2, vendor_code=VC, api_secret=APP_KEY, imei=IMEI)

def parse_datetime(date_str):
    formats = ["%d-%m-%Y %I:%M %p", "%d-%m-%Y %H:%M"]
    for fmt in formats:
        try:
            return dt_datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date parsing error: time data '{date_str}' does not match any of the known formats.")

def extract_stock_list_from_csv(csv_file_path, target_datetime_str):
    stock_list = []
    try:
        target_datetime = parse_datetime(target_datetime_str)
        target_date = target_datetime.date()
        target_time = target_datetime.time()

        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row_datetime = parse_datetime(row['date'])
                except ValueError:
                    continue

                if row_datetime.date() == target_date and row_datetime.time() == target_time:
                    stock_list.append(f"{row['symbol']}-EQ")
    except Exception as e:
        logging.error(f"An error occurred while extracting stock list: {e}")
    logging.info(f"Extracted stock list: {stock_list}")
    return stock_list

def place_orders(target_datetime_str):
    global stocksList, slArray, tgtArray

    stocksList = extract_stock_list_from_csv(CSV_FILE_PATH, target_datetime_str)
    stocksList = [symbol for symbol in stocksList if symbol not in REMOVE_STOCKS]

    if len(stocksList) > 3:
        stocksList = []
        logging.info("More than 3 stocks found. No orders will be placed.")
    elif not stocksList:
        slArray = []
        tgtArray = []
        logging.info("No stocks found for the given time. Clearing previous stock lists.")
    else:
        slArray = []
        tgtArray = []

        for symbol in stocksList:
            try:
                quote = api.get_quotes(exchange='NSE', token=symbol)
                LTP = float(quote["lp"])

                stop_loss = round(LTP * 1.0045, 2)
                target = round(LTP * 0.992, 2)
                Qty_Stock = round(10000 / LTP)
                slArray.append(stop_loss)
                tgtArray.append(target)

                logging.info(f"LTP: {LTP}, Stop-Loss: {stop_loss}, Target: {target} for symbol: {symbol}")

                api.place_order(
                    buy_or_sell='S', product_type='I', exchange='NSE', tradingsymbol=symbol,
                    quantity=Qty_Stock, discloseqty=0, price_type='MKT', trigger_price=None,
                    retention='DAY', remarks='Place_order'
                )
                logging.info(f"Order placed for symbol: {symbol} (Qty: {Qty_Stock}, Stop-Loss: {stop_loss}, Target: {target})")

            except Exception as e:
                logging.error(f"Error occurred for symbol {symbol}: {e}")

    logging.info("place_orders function completed.")

def load_global_variables():
    global stock_names, rpnl_values, quantities
    logging.debug("Running load_global_variables")
    try:
        positions = api.get_positions()
        df = pd.DataFrame(positions)
        if 'tsym' not in df.columns or 'rpnl' not in df.columns or 'daysellqty' not in df.columns:
            logging.error("No positions data found or data is not in the expected format.")
            return

        stock_names = df['tsym'].dropna().tolist()
        rpnl_values = pd.to_numeric(df['rpnl'], errors='coerce').fillna(float('nan')).tolist()
        quantities = pd.to_numeric(df['daysellqty'], errors='coerce').fillna(0).astype(int).tolist()

        if not stock_names:
            logging.info("No stock positions found.")
            return

        log_message = (f"Loaded variables:\n"
                       f"Stock Names: {stock_names}\n"
                       f"PnL Values: {rpnl_values}\n"
                       f"Quantities: {quantities}")
        logging.info(log_message)
        print(log_message)  # Print to terminal as well

    except Exception as e:
        logging.error(f"Error loading global variables: {e}")

def place_buy_orders_based_on_positions():
    global stock_names, rpnl_values, quantities
    logging.debug("Running place_buy_orders_based_on_positions")
    
    for i in range(len(stock_names)):
        if stock_names[i] in processed_stocks:
            continue

        if rpnl_values[i] is not None and (rpnl_values[i] <= -40 or rpnl_values[i] >= 79):
            try:
                ret = api.place_order(
                    buy_or_sell='B',
                    product_type='I',
                    exchange='NSE',
                    tradingsymbol=stock_names[i],
                    quantity=quantities[i],
                    discloseqty=0,
                    price_type='MKT',
                    retention='DAY',
                    remarks='my_order_001'
                )
                processed_stocks.add(stock_names[i])
                logging.info(f"Buy order placed for {stock_names[i]}. Quantity: {quantities[i]}, PnL: {rpnl_values[i]}")
            except Exception as e:
                logging.error(f"Error placing buy order for {stock_names[i]}: {e}")

def round_down_to_nearest_15_minutes(dt):
    new_minute = (dt.minute // 15) * 15
    return dt.replace(minute=new_minute, second=0, microsecond=0)

def get_previous_timestamp():
    now = dt_datetime.now()
    previous_time = now - timedelta(minutes=15)
    rounded_time = round_down_to_nearest_15_minutes(previous_time)
    return rounded_time.strftime('%d-%m-%Y %I:%M %p')

def schedule_place_orders(start_time, end_time):
    current_time = dt_datetime.now()
    next_call_time = dt_datetime.combine(current_time.date(), start_time)
    
    while dt_datetime.now().time() <= end_time:
        now_time = dt_datetime.now()
        
        if now_time >= next_call_time:
            target_datetime_str = get_previous_timestamp()
            logging.info(f"Placing orders for {target_datetime_str} at {now_time.time()}")
            place_orders(target_datetime_str)
            
            next_call_time += timedelta(minutes=15)  # Schedule next call after 15 minutes
        else:
            time.sleep(1)  # Wait until the start time is reached

def schedule_load_global_variables(start_time, end_time):
    global last_logged_time
    current_time = dt_datetime.now()
    next_call_time = dt_datetime.combine(current_time.date(), start_time)
    
    while dt_datetime.now().time() <= end_time:
        now_time = dt_datetime.now()
        
        if now_time >= next_call_time:
            logging.info(f"Loading global variables at {now_time.time()}")
            load_global_variables()
            
            next_call_time += timedelta(minutes=15)  # Schedule next call after 15 minutes
        else:
            time.sleep(1)  # Wait until the start time is reached

def schedule_place_buy_orders_based_on_positions(start_time, end_time):
    current_time = dt_datetime.now()
    next_call_time = dt_datetime.combine(current_time.date(), start_time)
    
    while dt_datetime.now().time() <= end_time:
        now_time = dt_datetime.now()
        
        if now_time >= next_call_time:
            logging.info(f"Checking positions and placing orders at {now_time.time()}")
            place_buy_orders_based_on_positions()
            
            next_call_time += timedelta(seconds=5)  # Schedule next call after 5 seconds
        else:
            time.sleep(1)  # Wait until the start time is reached

if __name__ == "__main__":
    # Custom Start and End Times
    place_orders_start_time = dt_datetime.strptime("10:15", "%H:%M").time()
    place_orders_end_time = dt_datetime.strptime("11:46", "%H:%M").time()
    load_global_variables_start_time = dt_datetime.strptime("10:17", "%H:%M").time()
    load_global_variables_end_time = dt_datetime.strptime("11:47", "%H:%M").time()
    check_positions_start_time = dt_datetime.strptime("10:18", "%H:%M").time()
    check_positions_end_time = dt_datetime.strptime("15:10", "%H:%M").time()

    # Start place_orders function on a separate thread
    place_orders_thread = threading.Thread(target=schedule_place_orders, args=(place_orders_start_time, place_orders_end_time))
    place_orders_thread.start()

    # Start load_global_variables function on another thread
    load_global_variables_thread = threading.Thread(target=schedule_load_global_variables, args=(load_global_variables_start_time, load_global_variables_end_time))
    load_global_variables_thread.start()

    # Start place_buy_orders_based_on_positions function on another thread
    place_buy_orders_thread = threading.Thread(target=schedule_place_buy_orders_based_on_positions, args=(check_positions_start_time, check_positions_end_time))
    place_buy_orders_thread.start()

    place_orders_thread.join()
    load_global_variables_thread.join()
    place_buy_orders_thread.join()
