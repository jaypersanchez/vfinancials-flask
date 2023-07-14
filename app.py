from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import numpy as np
import os
import openai
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
openai_api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = openai.api_key = openai_api_key
#model_engine = "text-embedding-ada-002"
model_engine = "gpt-4"
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
from flask import Flask
from flask_cors import CORS
from openbb_terminal.sdk import openbb
import sys
import pandas as pd


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

### News top 10 headlines
@app.route('/news-headlines', methods=['GET'])
def newsHeadlines():
    url = 'https://newsapi.org/v2/everything?q=canadian politics&apiKey=06b87cc37802434492aab1085f401232'
    response = requests.get(url)

    # Check it was successful
    if response.status_code == 200: 
            # Show the data
            print(response.json())
    else:
            # Show an error
            print('Request Error')
    
    return jsonify(response.json())

#### Crypto Endpoints ####
@app.route('/crypto/swaps', methods=['GET'])
def crypto_swap():
    global swap_df
    try:
        swap_df = pd.DataFrame(openbb.crypto.defi.swaps()) #default list last 100 swaps
        swap_df.head()
        print(swap_df)
        print("/crypto/swaps")
    except HTTPError as e:
        print("Error:", e.reason)
    return swap_df.to_json(orient='records' )

@app.route('/crypto/erc20',methods=['GET'])
def crypto_erc20():
    global erc_df
    try:
        erc_df = pd.DataFrame(openbb.crypto.onchain.erc20_tokens())
        erc_df.head()
        print(erc_df)
    except HTTPError as e:
        print("Error", e.reason)
    return erc_df.to_json(orient='records')

@app.route('/crypto/nft/collections', methods=['GET'])
def displayNFTCollections():
        global nft_df
        try:
            nft_df = pd.DataFrame(openbb.crypto.nft.collections())
            nft_df.head()
            print(nft_df)
        except HTTPError as e:
            print("Error", e.reason)
        return nft_df.to_json(orient='records')
    
@app.route('/crypto/find', methods=['GET'])
def cryptoFind():
        global crypto_df
        print('/crypto/find')
        try:
            symbol = request.args.get('symbol')
            print("Selected symbol: %s" % symbol)
            #crypto_df = pd.DataFrame(openbb.crypto.find("eth", "CoinGecko", "name", 25))
            crypto_df = pd.DataFrame(openbb.crypto.find(symbol))
            crypto_df.head()
            print(crypto_df)   
        except HTTPError as e:
            print("Error", e.reason)
        return crypto_df.to_json(orient='records')

# The default list endpoint returns a list of forex pairs, stablecoin pairs and popular stock symbols with current price
@app.route('/default/forex', methods=['GET'])
def defaultForex():
        url = 'https://www.freeforexapi.com/api/live'
        #url = 'https://www.freeforexapi.com/api/live?pairs=USDCAD,USDJPY,EURUSD'
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
        response = requests.get(url)

        # Check it was successful
        if response.status_code == 200: 
            # Show the data
            print(response.json())
        else:
            # Show an error
            print('Request Error')
    
        #return jsonify(response.json())
        return jsonify(tickers)

@app.route('/default/crypto', methods=['GET'])
def defaultCrypto():
       tickers = ['AAVE', 'ADA', 'ALGO', 'AMP', 'APE', 'ATOM', 'AVAX', 'AXS', 'BCH', 'BNB',
                    'BTC', 'CRO', 'DOGE', 'DOT', 'EOS', 'ETH', 'FTM', 'GRT', 'LUNA', 'MATIC',
                    'NEO', 'NEXO', 'ONE', 'OMG', 'SOL', 'UNI', 'USDC', 'USDT', 'VET', 'XLM',
                    'XRP', 'XTZ', 'YFI']
       erc_df = pd.DataFrame(openbb.crypto.onchain.erc20_tokens()) 
       print(erc_df)
       return jsonify(tickers)
    
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
    
#Requires API_GLASSNODE_KEY
@app.route('/crypto/actively-traded', methods=['GET'])
def cryptoGetActivelyTraded():
    global active_df
    try:
        symbol = request.args.get('symbol')
        print("Selected symbol: %s" % symbol)
        active_df = pd.DataFrame(openbb.crypto.dd.active(symbol))
        active_df.head()
        print(active_df)
    except HTTPError as e:
         print("Error", e.reason)
    return active_df.to_json(orient='records')
             
@app.route('/crypto/graph', methods=['GET'])
def cryptoGraph():
    global chart_df_df
    global chart_fig
    try:
       symbol = request.args.get('symbol')
       print("Selected symbol: %s" % symbol)
       chart_df = openbb.crypto.candle(symbol={symbol},external_axes=True)
       chart_fig = chart_df.iplot(asFigure=True, kind='candle', xTitle='Time interval', yTitle='Price', title='Cryptocurrency Market', template="simple_white")
       print("showing chart")
       chart_fig.show()
       #chart_df_df = pd.DataFrame(chart_fig)
       #chart_df.update_layout(template="seaborn")
       #chart_df_df.head()
       #chart_df.head()
    except HTTPError as e:
         print("Error", e.reason)
    return "Success" #jsonify(chart_df_df.to_dict())

#### Crypto Endpoints ####

# Stocks Endpoints #
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
    print(f"/stocks/search {selectedCountry}::{selectedExchange}")
    #return(f"/stocks/search {selectedCountry}::{selectedExchange}")
    return jsonify(stocks_df.to_json(orient='index'))
    

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
# Stocks Endpoints #
        
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
    url = "https://api.openai.com/v1/engines/text-davinci-003/completions"
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
    app.run()