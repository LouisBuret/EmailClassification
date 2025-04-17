from flask import Flask, render_template, request
import keras
from tensorflow import keras
from keras.saving import load_model
import spacy
import pandas as pd

nlp = spacy.load('en_core_web_lg')

def preprocess(email : str) -> list:
    vectors = []
    doc = nlp(email)
    vectors.append(doc.vector)
    vector_df = pd.DataFrame(vectors) 
    return vector_df

model = load_model("99254.keras", )

def email_classifier(email : str) -> str:
    data = preprocess(email)
    return 'safe' if model.predict(data) < 0.5 else 'not safe'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) 
def index():
    if request.method == 'POST':
        mail = request.form['mail']
        print('ok')
        return render_template('response.html', response = email_classifier(mail))
    else:
        return render_template('start.html')

if __name__ == "__main__":
    app.run(debug=True, port=8081)