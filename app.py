from flask import Flask, render_template
from bls import fetch_bls_data, process_bls_data

app = Flask(__name__)

@app.route('/')
def index():
    bls_data = fetch_bls_data()
    items = process_bls_data(bls_data)
    return render_template("index.html", items=items)
