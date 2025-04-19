from flask import Flask, request
import logging
from translate import Translator
import json
app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

@app.route('/post', methods=['POST'])
def main():

    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):

    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Я могу переводить слова'
        return

    elif req['request']['original_utterance'].lower() in ['переведите слово', 'переведи слово']:
        words = req['request']['original_utterance'].lower().split('переведи слово')[-1].strip()

        # Переводим с русского на английский
        try:
            translator = Translator(from_lang="ru", to_lang="en")
            translation = translator.translate(words)
            res['response']['text'] = translation.lower()
            return
        except Exception as e:
            res['response']['text'] = "Не удалось перевести слово. Попробуйте ещё раз."
            return


if __name__ == '__main__':
    app.run()
