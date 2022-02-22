import data as dt
from flask import Flask



app = Flask(__name__)

 

@app.route('/')
def index():
    return dt.arr

app.run(debug = True , host = "0.0.0.0",port = 5100)


