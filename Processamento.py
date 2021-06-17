import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
import string
from nomes_brasileiros import *

lista_nome = lista_nomes()

def dict_to_list(dict):
    lista_tweets = []
    for item in dict:
        lista_tweets.append(item["text"])
    return lista_tweets


def process_tweet(tweet, lista_names=lista_nome):
    """Função de processamento de um tweet.
    Input:
        tweet: a string contendo o tweet
    Output:
        tweets_clean: uma lista de palavras contendo o tweet processado

    """
    # pegando lista de palavras stopwords
    stopwords_portuguese = stopwords.words('portuguese')

    # remove tickers do mercado de ações como $ GE
    tweet = re.sub(r'\$\w*', '', tweet)

    # remove o texto retweetado no estilo antigo "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)

    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)

    # remove hashtags
    tweet = re.sub(r'#', '', tweet)

    # remove os @
    tweet = re.sub(r'@', '', tweet)

    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)

    tweets_clean = []

    for word in tweet_tokens:
        if (word not in stopwords_portuguese and  # remove stopwords
                word not in string.punctuation and  # remove pontuação
                word not in lista_names):  # remove nomes

            tweets_clean.append(word)

    return tweets_clean

