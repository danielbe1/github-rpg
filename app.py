import logging
import os
import sys

from flask import Flask
from flask import request

from github.github_api import GithubWebhookHandler
from habitica.habitica_api import HabiticaAPIClient

app = Flask(__name__)
habitica_api_client = HabiticaAPIClient()
github_webhook_handler = GithubWebhookHandler(
    habitica_api_client,
    os.environ.get('LABEL_TO_IGNORE', 'github-rpg-ignore'))


@app.route('/', methods=['POST'])
def handle_github_webhook():
    try:
        github_webhook_handler.handle_webhook(request)
    except Exception as e:
        print(str(e))

    return 'success'

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info('Service starting....')

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
