function getRiddle() {
            return [
                document.getElementById('riddle').value,
                document.getElementById('answer').value,
            ];
        }

async function addRiddle() {
    const [riddle, answer] = getRiddle();
    const initialResponse = await fetch(`/addRiddle`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            riddle: riddle,
            answer: answer
        }),
    });
    const response = await initialResponse.json();

}
