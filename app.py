import morfeusz2 as morf
from flask import Flask, request, jsonify

morph = morf.Morfeusz()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/conjugate', methods=['GET'])


def conjugate():
    verb = request.args.get('verb')
    print(verb)
    if verb is None:
        return jsonify({'error': 'No verb provided'})

    analysis = morph.analyse(verb)


    print(analysis)

    forms = set()
    for interpretation in analysis:
        lemma = str(interpretation[1])  # get the lemma
        tag_id = interpretation[0]  # get the tag id

        generated_forms = morph.generate(lemma, tag_id)

        print(generated_forms)

        for form in generated_forms:
            forms.add(form[0])
            if form[0].endswith('by') and form[0][:-2] not in forms:
                forms.add(form[0][:-2])  # add the form without 'by' if it's not already present

    # add conditional forms
    if 'by' in forms:
        forms.add('by ' + verb)
        if verb.endswith('ć'):
            forms.add('by ' + verb[:-1] + 'ła')
            forms.add('by ' + verb[:-1] + 'ło')
            forms.add('by ' + verb[:-1] + 'ły')
        else:
            forms.add('by ' + verb + 'a')
            forms.add('by ' + verb + 'o')
            forms.add('by ' + verb + 'y')

    return jsonify({'verb': verb, 'conjugations': list(forms)})



if __name__ == '__main__':
    app.run()


