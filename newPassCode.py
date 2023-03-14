import requests as req
from bs4 import BeautifulSoup as BS
import numpy as np
import json
import re
import sys
from nltk.stem import PorterStemmer as PS
from gensim.parsing.preprocessing import remove_stopwords

low_ = int(sys.argv[1])
high_ = int(sys.argv[2])

ps = PS()

alpha_l = "abcdefghijklmnopqrstuvwxyz"
alpha_c = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
number = "0123456789"
sym = "!@#*&%$"

def prob(j):
    return np.random.randint(j)/j

asks = ["Can","Cannot","Can't","can","should","Should","if","If",
        "cannot","can't","could","couldn't",
        "Could","Couldn't","Are","are","ought","Ought",
        "Aren't","aren't","what","What","Where","where","when",
        "When","Why","why","how","How","Whom","whom","who","Who",
        "Will","will","Won't","won't"
        ]

index = np.random.randint(2,1000001)

def removeEmpty(txtlist):
    return [i for i in txtlist if i != ""]

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def textDuplicate(text):
    txt = text.split(" ")
    return list(dict.fromkeys(txt))

def remove_punctuation(text):
    clean = re.compile("[^\w\s]")
    return re.sub(clean,' ',text)

def remove_stops(text):
    txt = remove_stopwords(text)
    return txt

def tp(txt):
    txt = remove_html_tags(txt)
    txt = remove_punctuation(txt)
    txt = remove_stops(txt)
    txt = textDuplicate(txt)
    txt = removeEmpty(txt)
    txt = [i for i in txt if i not in asks]
    txt = [ps.stem(i) for i in txt]
    return txt

def getJson(url):
    return req.get(url)

def fourA(j):
    import random
    rand = random.uniform(0,1)
    rest = (1 - rand)/3
    b = rand + rest
    c = rand + rest * 2
    d = rand + rest * 3
    if j <= rand:
        target = np.random.randint(len(alpha_l))
        out = alpha_l[targert]
        return out
    elif j > rand and j <= b:
        target = np.random.randint(len(alpha_c))
        out = alpha_c[target]
        return out
    elif j > b and j <= c:
        target = np.random.randint(len(number))
        out = number[target]
        return out
    else:
        target = np.random.randint(len(sym))
        out = sym[target]
        return out

def judge(string):
    text =string
    if len(text) >= low_ and len(text) <= high_:
        print("".join(text))
    elif len(text) > high_:
        while len(text) > high_-1:
            target = np.random.randint(len(text))
            text = text[:target]+text[target+1:]
        target = np.random.randint(len(text))
        text = text[:target]+sym[np.random.randint(len(sym))]+text[target:]
        print(text)
    else:
        addon = fourA(prob(100))
        while len(text) < low_-1:
            target = np.random.randint(len(text))
            text = text[:target] + addon + text[target:]
        target = np.random.randint(len(text))
        text = text[:target]+sym[np.random.randint(len(sym))]+text[target:]
        print(text)

if __name__ == "__main__":
    data = getJson("https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(index))
    if data.status_code == 200:
        _json = data.json()
        if "url" in _json.keys():
            soup = BS(getJson(_json["url"]).content,"html5lib")
            final_t = []
            p = soup.find_all("p")
            for i in p:
                final_t.append(i.text)
            final_t = "".join(final_t)
            txt = tp(final_t)
            txt_ = ["".join(dict.fromkeys(i)) for i in txt]
            txt = [txt[i] for i in range(len(txt)) if txt[i] == txt_[i]]
            text = "".join(txt)
            judge(text)
        else:
            text = tp(_json["text"])
            text_ = ["".join(dict.fromkeys(i)) for i in text]
            text = [text[i] for i in range(len(text)) if text[i] == text_[i]]
            text = "".join(text)
            judge(text)
