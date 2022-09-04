async function verify(id) {
    const answer = document.getElementById(`input-${id}`);
    const initialResponse = await fetch(`/getAnswer`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            answer: answer.value,
            id: id.toString(),
        }),
    });
    const response = await initialResponse.json();
    response['correct'] ? answer.classList.add('answer-true'): answer.classList.add('answer-false');
}
