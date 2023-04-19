from flask import Flask, jsonify, request
from reverso_api.context import ReversoContextAPI

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/conjugate', methods=['GET'])
def conjugate_verb():
    verb = request.args.get('verb')
    api = ReversoContextAPI(verb, source_lang='pol', target_lang='eng')
    print(api)
    print(verb)
    inflected_forms = []
    for source_word, translation, frequency, part_of_speech, forms in api.get_translations():
        
        if forms:
            inflected_forms.extend([form.translation for form in forms])
    return jsonify(inflected_forms)

if __name__ == '__main__':
    app.run(debug=True)