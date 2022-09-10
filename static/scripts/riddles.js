window.addEventListener('DOMContentLoaded', async (event) => {
    for (let id = 1; id < document.getElementsByTagName('button').length; id++) {
        const userAnswer = JSON.parse(localStorage.getItem(`userAnswer-${id}`))
        if (userAnswer !== null) {
            const answer = document.getElementById(`input-${id}`);
            answer.value = userAnswer[1];
            answer.classList.add(`answer-${userAnswer[2]}`);
        }
    }
    for (const button of document.getElementsByTagName('button')) {
        button.addEventListener('click', () => verify(button.id));
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
    answer.classList.add(`answer-${response['correct']}`)
    localStorage.setItem(`userAnswer-${id}`, JSON.stringify([id, answer.value, response['correct']]))
}
