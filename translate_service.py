from flask import Flask, request, jsonify, render_template
import boto3
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data['text']
    source_lang = data['sourceLang']
    target_lang = data['targetLang']

    translate = boto3.client(service_name='translate', region_name='ap-south-1')

    try:
        result = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        return jsonify({
            'translatedText': result['TranslatedText'],
            'sourceLanguage': result['SourceLanguageCode'],
            'targetLanguage': result['TargetLanguageCode']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
