# source c:/Users/alexm/Flask/morfeusz/venv/Scripts/activate
from flask import Flask, request, jsonify
import nltk
from nltk.corpus import toolbox


app = Flask(__name__)

nltk.download('toolbox', download_dir='.')

@app.route('/conjugate', methods=['GET'])
def conjugate():
    verb = request.args.get('verb')
    if verb is None:
        return jsonify({'error': 'No verb provided'})

    lexicon = nltk.corpus.toolbox.xml('lexicon.xml')

    # lexicon = toolbox.xml('iu_mien_samp.xml')


    # search for the entry with the given lemma
    for entry in lexicon:
        if entry.get('part_of_speech') == 'verb' and entry.find('l').text == verb:
            paradigm = entry.find('paradigm')
            if paradigm is None:
                return jsonify({'error': 'No conjugations found'})
            else:
                forms = [form.text for form in paradigm.findall('i')]
                return jsonify({'verb': verb, 'conjugations': forms})

    return jsonify({'error': 'Verb not found'})

if __name__ == '__main__':
    app.run()