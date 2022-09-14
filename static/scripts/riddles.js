window.addEventListener('DOMContentLoaded', async (event) => {
    for (let [key, value] of Object.entries(localStorage)) {
        const data = JSON.parse(value);
        const answer = document.getElementById(`input-${data[0]}`);
        answer.value = data[1];
        answer.classList.add(`answer-${data[2]}`);
    }
    for (const button of document.getElementsByTagName('button')) {
        button.addEventListener('click', button.id !== 'add' ? () => verify(button.id) : addRiddle);
    }
});

async function verify(id) {
    const answer = document.getElementById(`input-${id}`);
    const initialResponse = await fetch(`/verifyAnswer?`  + new URLSearchParams({
        id,
        answer: answer.value,
    }), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    const response = await initialResponse.json();
    answer.classList.add(`answer-${response['correct']}`);
    localStorage.setItem(`userAnswer-${id}`, JSON.stringify([id, answer.value, response['correct']]));
}

function newData() {
    return [
        document.getElementById('newRiddle').value,
        document.getElementById('newAnswer').value,
    ];
}

async function addRiddle() {
    const [riddle, answer] = newData();
    const initialResponse = await fetch(`/addRiddle`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            riddle,
            answer,
        }),
    });
    let riddles = document.getElementById("riddles");
    let block = document.createElement("div");
    block.className = "block";
    let riddleElement = document.createElement("div");
    riddleElement.className = "riddle";
    riddleElement.innerHTML = riddle;
    let answerElement = document.createElement("div");
    answerElement.className = "answer";
    let inputElement = document.createElement("input");
    inputElement.type = "text";
    const buttons = document.getElementsByTagName('button');
    const newId = parseInt(buttons.item(buttons.length-2).id)+1;
    inputElement.id = `input-${newId}`;
    let buttonElement = document.createElement("button");
    buttonElement.id = `${newId}`;
    buttonElement.innerHTML = "Перевірити";
    riddles.prepend(block);
    block.appendChild(riddleElement);
    block.appendChild(answerElement);
    answerElement.appendChild(inputElement);
    answerElement.appendChild(buttonElement);
    buttonElement.addEventListener('click', () => verify(buttonElement.id));
}