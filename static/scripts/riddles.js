window.addEventListener('DOMContentLoaded', async (event) => {
    for (const [key, value] of Object.entries(localStorage)) {
        const data = JSON.parse(value);
        const answer = document.getElementById(`input-${data[0]}`);
        answer.value = data[1];
        answer.classList.add(`answer-${data[2]}`);
    }
    for (const input of document.getElementsByTagName('input')) {
        input.addEventListener('input', input.id !== 'newAnswer' ? () => classReset(input.id) : void(0));
    }
    for (const button of document.getElementsByTagName('button')) {
        button.addEventListener('click', button.id !== 'add' ? () => verify(button.id) : addRiddle);
    }
});


async function classReset(id) {
    document.getElementById(id).className = '';
}


async function verify(id) {
    const answer = document.getElementById(`input-${id}`);
    const initialResponse = await fetch('/verifyAnswer?'  + new URLSearchParams({
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


async function addRiddle() {
    const riddle = document.getElementById('newRiddle').value;
    const answer = document.getElementById('newAnswer').value;
    const initialResponse = await fetch('/addRiddle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            riddle,
            answer,
        }),
    });
    const id = await initialResponse.json();
    const riddles = document.getElementById('riddles');
    const block = document.createElement('div');
    block.className = 'block';
    const riddleElement = document.createElement('div');
    riddleElement.className = 'riddle';
    riddleElement.innerHTML = riddle;
    const answerElement = document.createElement('div');
    answerElement.className = 'answer';
    const inputElement = document.createElement('input');
    inputElement.type = 'text';
    inputElement.id = `input-${id}`;
    const buttonElement = document.createElement('button');
    buttonElement.id = `${id}`;
    buttonElement.innerHTML = 'Перевірити';
    riddles.insertBefore(block, riddles.children[riddles.children.length-2]);
    block.appendChild(riddleElement);
    block.appendChild(answerElement);
    answerElement.appendChild(inputElement);
    answerElement.appendChild(buttonElement);
    inputElement.addEventListener('input', () => classReset(inputElement.id));
    buttonElement.addEventListener('click', () => verify(buttonElement.id));
}