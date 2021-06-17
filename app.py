###------------------ IMPORTANDO BIBLIOTECAS -------------------------###########

import sys
import pickle

from flask import Flask, render_template, request
from getting_data import TwitterClient
from Modelo_matematico import *

###-------------------- FIM DA IMPORTAÇÃO ------------------------------#############


###-------------------- Importando Banco de dados ----------------------#############
nltk.download('stopwords')
try:
    with open('Parametros/freqs.json', 'rb') as fp:
        freqs = pickle.load(fp)
except FileNotFoundError:
    print('Está faltando o modelo freqs.json')
    sys.exit(-1)

try:
    with open('Parametros/theta.json', 'rb') as fp:
        theta = pickle.load(fp)
except FileNotFoundError:
    print('Está faltando o modelo theta.json')
    sys.exit(-1)

lista_nome = lista_nomes()  # pct nomes brasileiros
freqs = freqs
theta = theta


###-------------------- Cria rotas  ----------------------#############
app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")


@app.route('/index_1.html', methods=["GET"])
def hello_word_1(predictions,legals,chatos):
    return render_template("index_1.html", prediction=predictions, legal=legals, chato=chatos)


@app.route('/', methods=['POST'])
def predict():
    # importando_tweets_recentes
    term = request.form['term']
    term = str(term)
    api = TwitterClient()
    tweets = api.get_tweets(query=term, count=500)
    tweets = dict_to_list(tweets)
    lista_tweet_positiva = []
    lista_tweet_negativa = []
    cont_neg = 0
    cont_pos = 0
    pontos_pos_corte = 0.75
    pontos_neg = 1.0
    tweet_legal = " "
    tweet_chato = " "
    for i in tweets:

        tweet_tratado = process_tweet(i, lista_names=lista_nome)
        stringu = ' '.join([str(item) for item in tweet_tratado])
        # print(stringu)
        y_hat = predict_tweet(stringu, freqs, theta)
        if y_hat >= 0.75:
            # print('Positive sentiment')
            cont_pos += 1
            lista_tweet_positiva.append(i)
            pontos_pos = y_hat
            if pontos_pos >= pontos_pos_corte:
                tweet_legal = str(i)
                pontos_pos_corte = pontos_pos
        else:
            # print('Negative sentiment')
            cont_neg += 1
            lista_tweet_negativa.append(i)
            if y_hat < pontos_neg:
                tweet_chato = str(i)
                pontos_neg = y_hat
    contador = (cont_pos, cont_neg)

    return render_template("index_1.html", prediction=contador, legal=tweet_legal, chato=tweet_chato)


'''
@app.route('/',methods=["cache"])
def cache():
'''

if __name__ == '__main__':
    app.run(port=3000, debug=True)
