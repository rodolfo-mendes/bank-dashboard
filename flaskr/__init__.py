import os
import pandas as pd

from flask import Flask, send_from_directory, render_template

def page_not_found(e):
        return render_template('404.html'), 404

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.register_error_handler(404, page_not_found)

    # preparig data
    df = pd.read_csv('data/bank-additional.csv', sep=";")
    df['conversion'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)
    
    @app.route('/')
    def index():
        model = {}
        model['total_clients'] = df.shape[0]
        model['total_conversions'] = df.conversion.sum()
        model['conversion_rate'] = (model['total_conversions'] / model['total_clients']) * 100
        return render_template('index.html', model=model)

    @app.route('/<path:path>')
    def send(path):
        return render_template(path + '.html')

    return app
