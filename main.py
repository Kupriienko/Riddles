from flask import Flask, jsonify, request, Response
import sqlite3
from localStoragePy import localStoragePy
import ast

localStorage = localStoragePy('riddleStorage', 'json')

app = Flask(__name__)

con = sqlite3.connect('r_database.sqlite', check_same_thread=False)
cur = con.cursor()


def riddles_amount() -> int:
    return cur.execute("select id from riddles order by id desc LIMIT 1;").fetchone()[0]


def answer_data(i: int) -> dict:
    try:
        return ast.literal_eval(localStorage.getItem("answer_data" + str(i)))
    except:
        return {"answer": "", "correct": ""}


def block_in_str(i: int) -> str:
    answer_d = answer_data(i)
    riddle = cur.execute("select riddle from riddles where id = ?", (i,)).fetchall()
    return f'''            <div class="block">
            <div class="riddle">{riddle[0][0]}</div>
            <div class="answer">
                <input type="text" name="answer" class="{answer_d["correct"]}" value="{answer_d["answer"]}" >
                <button>Перевірити</button>
            </div>
        </div>\n'''


def initial_content(r_amount: int) -> None:
    with open("index.html", "r") as f:
        contents = f.readlines()
    html_code = ""
    for i in range(1, r_amount + 1):
        html_code += block_in_str(i)
    contents.insert(18, html_code)
    with open("index.html", "w") as f:
        contents = "".join(contents)
        f.write(contents)


def answer_correct(correct: str, int_correct: int, data: dict, answer_d: str):
    data["correct"] = correct
    localStorage.setItem(answer_d, str(data))
    return {"correct": int_correct}


@app.route('/addRiddle', methods=['POST'])
def add_riddle() -> Response:
    data = request.get_json()
    riddle = [data["riddle"], data["answer"]]
    cur.execute("insert into riddles (riddle, solution) values (?, ?)", riddle)
    con.commit()
    return jsonify(
        riddle=riddle,
    )


@app.route('/getAnswer', methods=['GET'])
def get_answer() -> dict[str, int]:
    data = request.get_json()
    answer_d = "answer_data"+str(data[0])
    answer = cur.execute("select id, solution from riddles")
    for i in answer.fetchall():
        if i[0] == data["id"]:
            if i[1] == data["answer"]:
                return answer_correct("answer-true", 1, data, answer_d)
            else:
                return answer_correct("answer-false", 0, data, answer_d)


@app.route('/')
def index() -> str:
    initial_content(riddles_amount())
    with open('index.html', 'r') as contents:
        return contents.read()
