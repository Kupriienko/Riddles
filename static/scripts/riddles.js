async function verify(id) {
    const answer = document.getElementById(`input-${id}`);
    const initialResponse = await fetch(`/getAnswer?`  + new URLSearchParams({
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
