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
    
    