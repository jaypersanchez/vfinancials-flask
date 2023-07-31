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

def forexQuote(_symbol):
    global quote_df
    try:
        quote_df = openbb.forex.quote(_symbol)
        quote_df.head()
        return quote_df.to_json(orient='records' )
    except HTTPError as e:
        print("Error:", e.reason)
        return jsonify({"error": e.reason})
    
    