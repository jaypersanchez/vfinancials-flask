from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import numpy as np
import os
import openai
import requests
from dotenv import load_dotenv
load_dotenv()
#from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
openai_api_key = os.getenv('OPENAI_API_KEY')
#model_engine = "text-embedding-ada-002"
model_engine = "gpt-4"
#model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
from flask import Flask
from flask_cors import CORS
from openbb_terminal.sdk import openbb
import sys
import pandas as pd
newsApiKey = os.getenv('NEWS_API_KEY')

# modules
from modules import crypto
from modules import general
from modules import forex

#Test Data for embedding
documents = [
    "GB  EURONEXT    UK  -  REPORTING  SERVICES  DRSP  DRSP  WWW.EURONEXT.COM",
    "CA  CANADIAN  SECURITIES  EXCHANGE  XCNQ  XCNQ  WWW.THECSE.COM",
    "CA  CANADIAN  SECURITIES  EXCHANGE  -  PURE  PURE  XCNQ  WWW.THECSE.COM",
    "GB  ZODIA  MARKETS  ZODM  ZODM  WWW.ZODIA-MARKETS.COM",
    "US  FENICS  FX  ECN  FNFX  BGCF  WWW.FENICSFX.COM",
    "NO  NASDAQ  OSLO  ASA  NORX  NORX  WWW.NASDAQ.COM/SOLUTIONS/EUROPEAN-COMMODITIES",
    "ES  PORTFOLIO  STOCK  EXCHANGE  POSE  POSE  WWW.PORTFOLIO.EXCHANGE",
    "US  PUNDION  LLC  PUND  PUND  WWW.PUNDION.COM",
    "BG  UNICREDIT  BULBANK  AD  -  SYSTEMATIC  INTERNALISER  UCBG  UCBG  WWW.UNICREDITBULBANK.BG",
    "AU  ASX  -  NEW  ZEALAND  FUTURES  &  OPTIONS  NZFX  XASX  WWW.ASX.COM.AU",
    "US  ONECHICAGO  LLC  XOCH  XOCH  WWW.ONECHICAGO.COM",
    "SG  BONDBLOX  EXCHANGE  BBLX  BBLX  WWW.BONDBLOX.COM"
]

app = Flask(__name__)
CORS(app)
@app.route('/test/vectordata')
def generate_embeddings():
    document_embeddings = model.encode(documents)
    return str(document_embeddings)

@app.route('/test/document')
def get_documents():
    return str(documents)

@app.route('/mykeys')
def myKeys():
    print(openbb.keys.mykeys(show=True))


######################################### Forex Endpoints ####################################################

# get forex quote
@app.route('/forex/quote', methods=['GET'])
def forexQuote():
    try:
        symbol = request.args.get('symbol')
        quote_df = forex.forexQuote(symbol)
        return quote_df
    except HTTPError as e:
        print("Error:", e.reason)

######################################### Forext Endpoints ####################################################

######################################### Crypto Endpoints ####################################################

@app.route('/crypto/swaps', methods=['GET'])
def crypto_swap():
    try:
        swap_df = crypto.crypto_swap()
    except HTTPError as e:
        print("Error:", e.reason)
    
    return swap_df

@app.route('/crypto/erc20',methods=['GET'])
def crypto_erc20():
    try:
        erc_df = crypto.crypto_erc20()
        return erc_df
    except HTTPError as e:
        print("Error", e.reason)
        return jsonify({"error": e.reason})

@app.route('/crypto/nft/collections', methods=['GET'])
def displayNFTCollections():
        try:
            nft_df = crypto.displayNFTCollections()
            return nft_df
        except HTTPError as e:
            print("Error", e.reason)
            return jsonify({"error": e.reason})
    
@app.route('/crypto/find', methods=['GET'])
def cryptoFind():
        try:
            symbol = request.args.get('symbol')
            crypto_df = crypto.cryptoFind(symbol)
            return crypto_df
        except HTTPError as e:
            print("Error", e.reason)
            return jsonify({"error": e.reason})
    
@app.route('/crypto/price', methods=['GET']) #bug or need a newer SDK version. 
def cryptoPrice():
        try:
            _symbol = request.args.get('symbol')
            print("Selected symbol: %s" % _symbol)
            result = crypto.cryptoPrice(_symbol)
            return result
        except HTTPError as e:
            print("Error", e.reason)
            return jsonify({"error": e.reason})
        
#this method retrieves price for asset pairs - BTCUSD or BTCEUR is currently only supported
@app.route('/crypto/pair', methods=['GET'])
def cryptoPair():
        _symbol = request.args.get('symbol')
        response = crypto.cryptoPair(_symbol)
        return response

@app.route('/crypto/graph', methods=['GET'])
def cryptoGraph():
    symbol = request.args.get('symbol')
    chart_df = crypto.cryptoGraph(symbol)
    return chart_df.to_json()

#load function - when given specific symbol and other data, it will return a tabular format of open, close, high and low.  
@app.route('/crypto/load', methods=['GET'])
def cryptoLoad():
    symbol = request.args.get('symbol')
    print("cryptoLoad " + symbol)
    try:
       result = crypto.cryptoLoad(symbol)
       return jsonify(result)
    except HTTPError as e:
        print("Error", e.reason)
        return jsonify({"error": e.reason})
    #return jsonify(load_df.to_json())

        
######################################### Crypto Endpoints ####################################################

######################################### Default Endpoints - free subscription access level ####################################################
  
### News top 10 headlines
@app.route('/news-headlines', methods=['GET'])
def newsHeadlines():
    try:
        response = general.newsHeadlines()
        # Show the data
        return response
    except HTTPError as e:
        return jsonify({"error": e.reason})
  
# The default list endpoint returns a list of forex pairs, stablecoin pairs and popular stock symbols with current price
@app.route('/default/forex', methods=['GET'])
def defaultForex():
        try: 
            # Show the data
            response = general.defaultForex()
            return response
        except HTTPError as e:
            return jsonify({"error": e.reason})
    
        
@app.route('/default/crypto', methods=['GET'])
def defaultCrypto():
        try:
           response = crypto.defaultCrypto()
           return response
        except HTTPError as e:
            return jsonify({"error": e.reason})
        
######################################### Default Endpoints - free subscription access level ####################################################

######################################### Paid Subscription Endpoints - Normally requires API Key from source ###################################

#Requires API_GLASSNODE_KEY
@app.route('/crypto/actively-traded', methods=['GET'])
def cryptoGetActivelyTraded():
    global active_df
    try:
        symbol = request.args.get('symbol')
        #print("Selected symbol: %s" % symbol)
        active_df = pd.DataFrame(openbb.crypto.dd.active(symbol))
        active_df.head()
        #print(active_df)
        return active_df.to_json(orient='records')
    except HTTPError as e:
         print("Error", e.reason)
         return jsonify({"error": e.reason})
             
######################################### Paid Subscription Endpoints - Normally requires API Key from source ###################################


######################################### Stocks Endpoints ######################################################################################

@app.route('/default/stocks', methods=['GET'])
def defaultStocks():
       tickers = ['AAPL', 'ABBV', 'ABT', 'ACN', 'ADP', 'ADSK', 'AMAT', 'AMGN', 'AMZN', 'APA',
                    'APC', 'AT&T', 'AXP', 'BA', 'BAC', 'BDX', 'BMY', 'BRKB', 'BRK.A', 'BRK.B',
                    'C', 'CAT', 'CELG', 'CHM', 'CL', 'COF', 'COST', 'CRM', 'CSCO', 'CVS',
                    'DHR', 'DIS', 'DOV', 'DOW', 'DTE', 'EIX', 'EMR', 'EXC', 'EXPD', 'F',
                    'FB', 'FDX', 'FIS', 'FITB', 'FLS', 'GE', 'GOOG', 'GOOGL', 'GS', 'HAL',
                    'HON', 'HPQ', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'LLY', 'LMT', 'MA',
                    'MMM', 'MO', 'MSFT', 'MTD', 'RTN', 'SBUX', 'SO', 'SPG', 'T', 'TGT',
                    'UNH', 'UNP', 'UPS', 'V', 'VZ', 'WMT', 'XOM']
        
       return jsonify(tickers)

@app.route('/stocks/search', methods=['GET'])
def stock_loadSymbol():
    bodyRequest = request.get_json()
    selectedCountry = bodyRequest.get("selected_country")
    selectedExchange = bodyRequest.get("selected_exchange")
    try:
        global stocks_df
        stocks_df = openbb.stocks.search(country=selectedCountry, exchange_country=selectedExchange)
    except HTTPError as e:
        print("Error:",e.reason)
   
    return jsonify(stocks_df.to_json(orient='index'))

@app.route('/stocks/load', methods=['GET'])
def stock_load():
    symbols = request.args.get('symbol')
    print(f"/stocks/load {symbols}")
    try:
        global stocks_df
        stocks_df = openbb.stocks.load(symbols)
        stocks_df.head()
    except HTTPError as e:
        print("Error:",e.reason)
    
    return jsonify(stocks_df.to_json(orient='index'))

@app.route('/stocks/stockeodquote', methods=['GET'])
def stock_stockEODQuote():
    symbols = request.args.get('symbol')
    url = os.getenv("EOD_API_URL") + symbols + "?fmt=json&filter=last_close&api_token=" + os.getenv("EOD_API_TOKEN")
    print("EOD Stock Quote " + url)
    response = requests.get(url)
    # Check it was successful
    if response.status_code == 200: 
            # Show the data
            print(response.status_code)
            print(response.json())
    else:
            # Show an error
            print('Request Error')
    
    return jsonify(response.json())

#Requires API_KEY_FINANCIALMODELINGPREP 
@app.route('/stocks/quote', methods=['GET'])
def stock_getQuote():
    symbols = request.args.get('symbol')
    print(f"/stocks/quote {symbols}")
    # iterate through passed in symbols
    results = []
    quotes: object = []
    for symbol in symbols:
        # call stock quote api from OpenBB SDK
        #print(symbol)
        quote = openbb.stocks.quote(symbol).transpose()
        # append quote to results
        results.append(quote)
        
    return results

######################################### Stocks Endpoints ######################################################################################

######################################### AI Endpoints ######################################################################################
        
@app.route('/')
# AI endpoints #
@app.route('/semantic')
def semantic_search():
    top_k=1
    query = request.args.get('query') #request.get_json()
    #query = data['query']
    document_embeddings = model.encode(documents)
    query_embedding = model.encode([query])[0]
    similarities = cosine_similarity([query_embedding], document_embeddings)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    results = [(index, similarities[index]) for index in top_indices]
    result_list = []
    for index, similarity in results:
        #data = {"Document": documents[index]}
        #result_list.append(data)
        result_list =  [documents[index] for index, similarity in results]
    #format proper response using ChatGpt
    url = os.getenv("OPENAI_COMPLETION_URL")
    prompt = "Provide a proper natural response where the prompt is " + query + " and the response is the following " + str(result_list) + " and provide source links if possible"
    #prompt = query
    payload = {
        "prompt": prompt,
        "temperature": 0.9,
        "max_tokens": 500
    }
    headers = {
        "Content-type":"application/json",
        "Authorization": "Bearer " + openai.api_key
    }
    
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    completion = data["choices"][0]["text"]
    #response = format_response(query, result_list[0])
    return str(completion)

######################################### AI Endpoints ######################################################################################
    
@app.route('/')
def hello():
    return "Flask Server End"

@app.route('/get_data')
def get_data():
    data = {
        'name': 'John Doe',
        'age': 25
    }
    return jsonify(data)

@app.route('/put_data', methods=['PUT'])
def put_data():
    data = request.get_json()
    name = data['name']
    age = data['age']
    # Do something with the data
    return jsonify({'status': 'success', 'name':name,'age':age})
# AI endpoints #

if __name__ == '__main__':
    print("VFinancials Listening on " + os.getenv("SERVER_PORT"))
    app.run(host='0.0.0.0', port=os.getenv("SERVER_PORT"))