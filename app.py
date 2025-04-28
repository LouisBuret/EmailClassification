from flask import Flask, render_template, request
import keras
from tensorflow import keras
from keras.saving import load_model
import spacy
import pandas as pd

import re
import email
from bs4 import BeautifulSoup



nlp = spacy.load('en_core_web_lg')



def read_email_from_string(s):
    message = email.message_from_string(s)
    return message

def extract_email_body(message):
    if message.is_multipart():
        for part in message.walk():
            type_content = part.get_content_maintype()
            if type_content == 'text':
                message = part
                break
        else:
            return 'escapenonetext'

    if message.get('Content-Transfer-Encoding') == 'base64':
        try:
            body = message.get_payload(decode=True).decode()
        except:
            body = message.get_payload(decode=True).decode(encoding='ISO-8859-1')
    else:
        body = message.get_payload(decode=False)
    return body

def remove_html(s):
    soup = BeautifulSoup(s, 'lxml')
    for sp in soup(['script', 'style', 'head', 'meta', 'noscript']):
        sp.decompose()
    s = ' '.join(soup.stripped_strings)
    return s

def email_body_to_text(body):
    body = remove_html(body)
    punctuation = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
    body = re.sub('[{}]'.format(punctuation), ' ', body)
    body = re.sub('\n+', ' ', body)
    body = re.sub('\\s+', ' ', body)
    body = re.sub(r'[0-9]+', 'escapenumber', body)
    body = body.lower()
    body = re.sub(r'[a-z0-9]{20,}', 'escapelong', body)
    return body



def preprocess(mail : str) -> list:
    temp = email_body_to_text(mail)
    vectors = []
    doc = nlp(temp)
    vectors.append(doc.vector)
    vector_df = pd.DataFrame(vectors) 
    return vector_df



model = load_model("99254.keras", )



def email_classifier(mail : str) -> str:
    data = preprocess(mail)
    return 'safe' if model.predict(data) < 0.5 else 'not safe'



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) 
def index():
    if request.method == 'POST':
        mail = request.form['mail']
        return render_template('response.html', previous_mail = mail, response = email_classifier(mail))
    else:
        return render_template('start.html')

if __name__ == "__main__":
    app.run(debug=True, port=8081)