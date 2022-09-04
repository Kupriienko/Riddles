async function verify(id) {
    const answer = document.getElementById(`input-${id}`);
    const initialResponse = await fetch(`/getAnswer`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            answer: answer.value,
            id: id,
        }),
    });
    const response = await initialResponse.json();
    let selector = response['correct'] ? 'answer-true': 'answer-false';
    answer.classList.add(selector)
}
