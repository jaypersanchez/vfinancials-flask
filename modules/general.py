from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import numpy as np
import os
import requests
from openbb_terminal.sdk import openbb
import sys
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def newsHeadlines():
    url = os.getenv("NEWS_API_URL") + os.getenv("NEWS_API_KEY")
    print(url)
    # Check it was successful
    try: 
            response = requests.get(url)
            print(response.json())
            return response.json()
    except HTTPError as e:
        print("Error", e.reason)
        return jsonify({"error": e.reason})
    
def defaultForex():
        url = os.getenv("FOREX_API_LIVE")
        tickers = ['EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF', 'AUDUSD', 'USDCAD', 'NZDUSD', 
                   'EURGBP', 'EURJPY', 'GBPJPY', 'CHFJPY', 'EURCHF', 'GBPCHF', 'AUDJPY', 
                   'AUDNZD', 'AUDCAD', 'CADJPY', 'NZDJPY', 'GBPAUD', 'GBPCAD', 'GBPNZD', 
                   'EURAUD', 'EURCAD', 'EURNZD', 'USDHKD', 'USDSGD', 'USDTRY', 'USDZAR', 
                   'USDMXN', 'USDNOK', 'USDSEK', 'USDDKK', 'USDCNH', 'EURTRY', 'EURNOK', 
                   'EURSEK', 'EURDKK', 'EURHUF', 'EURPLN', 'AUDCHF', 'AUDHKD', 'AUDSGD', 
                   'AUDNZD', 'CADCHF', 'CADHKD', 'NZDCHF', 'NZDHKD', 'SGDJPY', 'SGDHKD', 
                   'HKDJPY', 'TRYJPY', 'ZARJPY', 'MXNJPY', 'NOKJPY', 'SEKJPY', 'DKKJPY', 
                   'CNHJPY', 'HUFJPY', 'PLNJPY']
        # Get the data
        #params = {'pairs': 'USDCAD,USDJPY,EURUSD'}
        global response
        #response = requests.get(url, params = params)
        # Check it was successful
        try: 
            response = requests.get(url)
            print(response)
            return response.json()
        except HTTPError as e:
            print("Error", e.reason)
            return jsonify({"error": e.reason})
        
    
    
    