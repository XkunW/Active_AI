from flask import Flask
from flask_restful import Resource, Api, reqparse
from datetime import datetime, timedelta
import json
import pymongo
import os, sys
import json

# cwd = os.path.dirname(__file__)
# sys.path.append(os.path.join(cwd, "../lib/birthday_parser"))

from active_ai import BirthdayParser
from active_ai import CityParser

app = Flask(__name__)
api = Api(app)

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'QueMachine'

# mongo_server = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)

parser = reqparse.RequestParser()
parser.add_argument('q_num', type=int)

parser.add_argument('session_id', type=int)
parser.add_argument('from', type=str)
parser.add_argument('timestamp', type=str)
parser.add_argument('content', type=str)

parser.add_argument('request_all', type=int)


class QuestionManger:
    q_num = None
    question_instance = None

    def __init__(self, q_num):
        self.q_num = q_num
        if q_num == 1:
            self.question_instance = BirthdayParser()
        elif q_num == 2:
            self.question_instance = CityParser()

    def ask(self):
        return self.question_instance.ask()

    def answer(self, sentence):
        # Send sentence to instance
        return json.dumps(self.question_instance.reply(sentence))


class Chat(Resource):
    # Session cache stores chat records in the layout below:
    # { "id": int,
    #   "message": [
    #       {
    #           "from"      : str,
    #           "timestamp" : int,
    #           "content"   : str,
    #       },
    #       ...
    #   ]
    # }
    message_cache = {}

    # live_session -> dict{ int(id) : QuestionManger}
    live_session = {}

    id = 1

    def get(self):
        args = parser.parse_args()
        new_id = self.id
        self.id += 1
        new_session = QuestionManger(args['q_num'])
        self.live_session[new_id] = new_session

        try:
            question = new_session.ask()
        except Exception:
            question = "Hello World!"

        self.message_cache[new_id] = {"session_id": new_id, "message": []}
        message_body = self.add_message(new_id, question, False)

        return message_body, 200, {'Access-Control-Allow-Origin': '*'}

    def post(self):
        args = parser.parse_args()

        if args['session_id'] in self.live_session:

            message_body = self.add_message(args['session_id'], args['content'], True)

            try:
                current_session = self.live_session[args['session_id']]
                answer = current_session.answer(args['content'])
            except Exception as Error:
                print(Error)
                answer = "World Hello!"

            message_body = self.add_message(args['session_id'], answer, False)

            return message_body, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            return None, 404, {'Access-Control-Allow-Origin': '*'}

    def add_message(self, id, sentence, who, time=datetime.now()):
        message_body = {
            "session_id": id,
            "from": who,
            "timestamp": int(time.timestamp()),
            "content": sentence,
        }

        self.message_cache[id]["message"].append(message_body)

        return message_body


api.add_resource(Chat, '/api/')

if __name__ == "__main__":
    app.run(debug=True)
