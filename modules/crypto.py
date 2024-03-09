import io
from flask import Flask, json, send_file
from flask import request
from flask import abort
from flask import jsonify
from httpx import HTTPError
from matplotlib import pyplot as plt
import numpy as np
import os
import requests
from openbb_terminal.sdk import openbb
import sys
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def cryptoLoad(_symbol):
    print("crypto.cryptoLoad " + _symbol)
    global loaded_df
    try:
        #must first load
        loaded_df = openbb.crypto.load(symbol=_symbol,to_symbol="usdt",start_date="2020-01-01", end_date = "2020-01-31" ,source="CCXT")
        return loaded_df.to_json()
    except HTTPError as e:
        print("Error", e.reason)
        return jsonify({"error": e.reason})

def cryptoGraphDisplay(_symbol, from_date, to_date):
    #first must load
    loaded_df = cryptoLoad(_symbol)
    # Call the openbb.crypto.candle function with the given dates
    chart_df = openbb.crypto.candle(symbol=_symbol, data=loaded_df, start_date=from_date, end_date=to_date, exchange='binance', to_symbol="", source='CCXT', volume=True, title=f"{_symbol} Price from {from_date} to {to_date}", external_axes=False, yscale='linear', raw=False)
    # Create a plot
    plt.figure()
    chart_df.plot()  # example, replace with your actual plotting code
    plt.title(f"{_symbol} Price from {from_date} to {to_date}")

    # Save it to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Return the buffer as a response
    return send_file(buf, mimetype='image/png')
    
def cryptoGraph(_symbol):
    loaded_df = cryptoLoad(_symbol)
    #chart_df = openbb.crypto.candle(_symbol, raw=True)
    chart_df = openbb.crypto.candle(symbol=_symbol, data = loaded_df, start_date='2020-01-01', end_date='2020-12-31', exchange='binance', to_symbol="usdt", source='CCXT', volume=True, title="Bitcoin Price over 2020", external_axes=False, yscale='linear', raw=True)
    return chart_df #jsonify(chart_df_dict)

def cryptoPair(_symbol):
        global response
        url = "https://api.api-ninjas.com/v1/cryptoprice"
        headers = {
            "X-Api-Key": os.getenv("NINJAS_API_KEY")
        }
        response = requests.get(url+"?symbol="+_symbol, headers=headers)
        # Check it was successful
        if response.status_code == 200: 
            # Show the data
            #print(response.json())
            return response
        else:
            # Show an error
            print('Request Error')
            return jsonify({"Error":"Request Error"})
        
def cryptoPrice(_symbol):
        global crypto_price
        global crypto_price_dict
        #print('/crypto/price')
        try:
            #print("Selected symbol: %s" % _symbol)
            crypto_price = openbb.crypto.price(symbol=_symbol)
            print(crypto_price)
            crypto_price_dict = dict(zip(('Symbol','Price', 'Change'), crypto_price))
        except HTTPError as e:
            print("Error", e.reason)
            return jsonify({"error": e.reason})
        return jsonify(crypto_price_dict)
    
#This function returns only the single asset - AAVE, BTC, ETH
def defaultCrypto():
       tickers = ['AAVE', 'ADA', 'ALGO', 'AMP', 'APE', 'ATOM', 'AVAX', 'AXS', 'BCH', 'BNB',
                    'BTC', 'CRO', 'DOGE', 'DOT', 'EOS', 'ETH', 'FTM', 'GRT', 'LUNA', 'MATIC',
                    'NEO', 'NEXO', 'ONE', 'OMG', 'SOL', 'UNI', 'USDC', 'USDT', 'VET', 'XLM',
                    'XRP', 'XTZ', 'YFI']
       #erc_df = pd.DataFrame(openbb.crypto.onchain.erc20_tokens()) 
       #print(erc_df)
       return jsonify(tickers)
    
def cryptoFind(_symbol):
        global crypto_df
        try:
            #print("Selected symbol: %s" % symbol)
            #crypto_df = pd.DataFrame(openbb.crypto.find("eth", "CoinGecko", "name", 25))
            crypto_df = pd.DataFrame(openbb.crypto.find(_symbol))
            crypto_df.head()
            #print(crypto_df)   
        except HTTPError as e:
            print("Error", e.reason)
        return crypto_df.to_json()
    
def displayNFTCollections():
        global nft_df
        try:
            nft_df = pd.DataFrame(openbb.crypto.nft.collections())
            nft_df.head()
        except HTTPError as e:
            print("Error", e.reason)
        
        return jsonify(json.loads(nft_df.to_json()))

    
def crypto_erc20():
    global erc_df
    try:
        erc_df = pd.DataFrame(openbb.crypto.onchain.erc20_tokens())
        erc_df.head()
        print(erc_df)
    except HTTPError as e:
        print("Error", e.reason)
    return erc_df.to_json(orient='records')

def crypto_swap():
    global swap_df
    try:
        swap_df = pd.DataFrame(openbb.crypto.defi.swaps()) #default list last 100 swaps
        swap_df.head()
        #print(swap_df)
        #print("/crypto/swaps")
    except HTTPError as e:
        print("Error:", e.reason)
        
    return swap_df.to_json(orient='records' )

