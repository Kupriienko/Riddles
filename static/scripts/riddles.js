window.addEventListener('DOMContentLoaded', (event) => {
    const buttons = document.getElementsByTagName("button");
    for (const button of buttons) {
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
}
