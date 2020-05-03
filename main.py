import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

import pysnooper

app = Flask(__name__)

@pysnooper.snoop()
def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()

@pysnooper.snoop()
def get_url(fact):
    payload = {'input_text': fact}
    response = requests.post('https://hidden-journey-62459.herokuapp.com/piglatinize/',
                             data=payload,
                             allow_redirects=False)
    url = response.headers['Location']

    return url

@pysnooper.snoop()
@app.route('/')
def home():
    fact = get_fact().strip()
    body = get_url(fact)

    return body#Response(response=body, mimetype="text/plain")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
