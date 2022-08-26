from flask import Flask, jsonify, request, Response
import sqlite3

app = Flask(__name__)

con = sqlite3.connect('r_database.sqlite', check_same_thread=False)
cur = con.cursor()


def riddles_amount() -> int:
    return cur.execute("select id from riddles order by id desc LIMIT 1;").fetchone()[0]


def get_riddle(i) -> str:
    return cur.execute("select riddle from riddles where id = ?", (i,)).fetchall()[0][0]


def block_in_str(i: int) -> str:
    return f'''            <div class="block">
            <div class="riddle">{get_riddle(i)}</div>
            <div class="answer">
                <input type="text" name="answer"" >
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
    answer = cur.execute("select id, solution from riddles")
    for i in answer.fetchall():
        if i[0] == data["id"]:
            if i[1] == data["answer"]:
                return {"correct": 1}
            else:
                return {"correct": 2}


@app.route('/')
def index() -> str:
    initial_content(riddles_amount())
    with open('index.html', 'r') as contents:
        return contents.read()
