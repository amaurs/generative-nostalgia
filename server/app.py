from flask import Flask
from flask import jsonify
import markovify
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

with open("boleros_es.txt") as f:
    text = f.read()
    text_model_es = markovify.Text(text)
with open("boleros_en.txt") as f:
    text = f.read()
    text_model_en = markovify.Text(text)

@app.route('/boleros/es')
def sentence_es():
    d = {'sentence':text_model_es.make_short_sentence(100)}
    return jsonify(d)

@app.route('/boleros/en')
def sentence_en():
    d = {'sentence':text_model_en.make_short_sentence(100)}
    return jsonify(d)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2303)