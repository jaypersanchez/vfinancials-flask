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

def cryptoLoad(_requestData):
    global loaded_df
    try:
        requestData = _requestData.get_json()
        #must first load
        symbol = requestData['symbol']
        to_symbol = requestData['to_symbol']
        startdate = requestData['start_date']
        enddate = requestData['end_date']
        source = requestData['source']
        # to_symbol seems to support only USDT and EUR.  Reflects the same from the terminal usage.
        print("Crypto Loading Data " + symbol + " " + to_symbol + " " + startdate + " " + enddate + " " + source  )
        loaded_df = openbb.crypto.load(symbol=symbol,to_symbol=to_symbol,start_date=startdate, end_date=enddate,source=source)
        #print(loaded_df.to_json)
        return loaded_df
    except HTTPError as e:
        print("Error", e.reason)
        return jsonify({"error": e.reason})

def cryptoGraph(_requestData):
    requestData = _requestData.get_json()
    #must first load
    symbol = requestData['symbol']
    to_symbol = requestData['to_symbol']
    startdate = requestData['start_date']
    enddate = requestData['end_date']
    source = requestData['source']
    exchange = requestData['exchange']
    volume = requestData['volume']
    title = requestData['title'] #default to tru
    external_axes = requestData['external_axes']
    yscale = requestData['yscale']
    raw = requestData['raw'] #default to false.  If True, then it's meant to return data.  If False, it's meant to display OpenBB default chart window
    loaded_df = cryptoLoad(_requestData)
    #chart_df = openbb.crypto.candle(_symbol)
    chart_df = openbb.crypto.candle(symbol=symbol, data = loaded_df, start_date=startdate, end_date=enddate, exchange=exchange, to_symbol=to_symbol, source=source, volume=volume, title=title, external_axes=external_axes, yscale=yscale, raw=raw)
    if raw == 'True':
        print("Returning Raw Graphing Data")
        return chart_df.to_json()
    elif raw == 'False':
        #meant to display as graph using OpenBB default window
        print("Display OpenBB Chart Window")
        return chart_df

#def cryptoGraph(_symbol):
#    loaded_df = cryptoLoad(_symbol)
    #chart_df = openbb.crypto.candle(_symbol, raw=True)
#    chart_df = openbb.crypto.candle(symbol=_symbol, data = loaded_df, start_date='2020-01-01', end_date='2020-12-31', exchange='binance', to_symbol="usdt", source='CCXT', volume=True, title="Bitcoin Price over 2020", external_axes=False, yscale='linear', raw=True)
#    return chart_df #jsonify(chart_df_dict)

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
            return response.json()
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
            #print(crypto_price[0])
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
            #print(nft_df)
        except HTTPError as e:
            print("Error", e.reason)
        
        return nft_df.to_json(orient='records')
    
def crypto_erc20():
    global erc_df
    try:
        erc_df = pd.DataFrame(openbb.crypto.onchain.erc20_tokens())
        erc_df.head()
        #print(erc_df)
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

