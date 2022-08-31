from flask import Flask, jsonify, request, Response, abort
import sqlite3

app = Flask(__name__)

con = sqlite3.connect('r_database.sqlite', check_same_thread=False)
cur = con.cursor()


@app.route('/addRiddle', methods=['POST'])
def add_riddle() -> tuple[str, str]:
    data = request.get_json()
    if type(data) != dict or data.keys() != {'riddle', 'answer'}:
        abort(400)
    riddle = data['riddle'], data['answer']
    cur.execute('insert into riddles (riddle, solution) values (?, ?)', riddle)
    con.commit()
    return riddle


@app.route('/getAnswer', methods=['GET'])
def get_answer() -> dict[str, bool]:
    data = request.get_json()
    if type(data) != dict or data.keys() != {'riddle', "id"}:
        abort(400)
    answer = cur.execute('select solution from riddles where id = ?', (data['id'],)).fetchall()
    if len(answer) == 1:
        return {'correct': answer[0][0] == data['answer']}
    else:
        abort(404)


@app.route('/')
def index() -> str:
    template_contents = open('index.html', 'r').read()
    riddle_contents = open('riddle.html', 'r').read()
    riddles = ''
    for i in cur.execute('select riddle from riddles').fetchall():
        riddles += riddle_contents.replace('{riddle}', i[0]) + '\n'
    return ''.join(template_contents.replace('{riddles}', riddles))
