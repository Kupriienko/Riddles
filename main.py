from flask import Flask, jsonify, request, Response, abort
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
con = psycopg2.connect(
    host='localhost',
    database='riddles.db',
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD'),
    port=5432
)
cur = con.cursor()


@app.route('/addRiddle', methods=['POST'])
def add_riddle() -> str:
    data = request.get_json()
    if type(data) != dict or data.keys() != {'riddle', 'answer'}:
        abort(400)
    riddle = data['riddle'], data['answer']
    cur.execute('insert into riddles (riddle, solution) values (%s, %s) returning id', riddle)
    con.commit()
    return str(cur.fetchone()[0])


@app.route('/verifyAnswer', methods=['GET'])
def get_answer() -> dict[str, bool]:
    data = request.args.to_dict()
    if type(data) != dict or (data.keys() != {'answer', 'id'} or not data['id'].isnumeric()):
        abort(400)
    cur.execute('select solution from riddles where id = %s', (data['id'],))
    answer = cur.fetchall()
    if len(answer) == 1:
        return {'correct': answer[0][0] == data['answer']}
    else:
        abort(404)


@app.route('/')
def index() -> str:
    index_template = open('index.html', 'r', encoding='utf-8').read()
    riddle_template = open('riddle.html', 'r', encoding='utf-8').read()
    riddles = ''
    cur.execute('select id, riddle from riddles')
    for i in cur.fetchall():
        riddles += riddle_template.replace('{id}', str(i[0])).replace('{riddle}', i[1]) + '\n'
    return ''.join(index_template.replace('{riddles}', riddles))
