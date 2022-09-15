from flask import Flask, jsonify, request, Response, abort
import sqlite3

app = Flask(__name__)

con = sqlite3.connect('r_database.sqlite', check_same_thread=False)
cur = con.cursor()


@app.route('/addRiddle', methods=['POST'])
def add_riddle() -> str:
    data = request.get_json()
    if type(data) != dict or data.keys() != {'riddle', 'answer'}:
        abort(400)
    riddle = data['riddle'], data['answer']
    cur.execute('insert into riddles (riddle, solution) values (?, ?)', riddle)
    con.commit()
    return str(cur.execute('select id from riddles where riddle = ?', (data['riddle'],)).fetchall()[0][0])


@app.route('/verifyAnswer', methods=['GET'])
def get_answer() -> dict[str, bool]:
    data = request.args.to_dict()
    if type(data) != dict or (data.keys() != {'answer', 'id'} or not data['id'].isnumeric()):
        abort(400)
    answer = cur.execute('select solution from riddles where id = ?', (data['id'],)).fetchall()
    if len(answer) == 1:
        return {'correct': answer[0][0] == data['answer']}
    else:
        abort(404)


@app.route('/')
def index() -> str:
    index_template = open('index.html', 'r', encoding='utf-8').read()
    riddle_template = open('riddle.html', 'r', encoding='utf-8').read()
    riddles = ''
    for i in cur.execute('select id, riddle from riddles').fetchall():
        riddles += riddle_template.replace('{id}', str(i[0])).replace('{riddle}', i[1]) + '\n'
    return ''.join(index_template.replace('{riddles}', riddles))
