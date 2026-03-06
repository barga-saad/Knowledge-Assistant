const fileInput = document.getElementById('file-input');
const uploadButton = document.getElementById('upload-button');
const chatHistory = document.getElementById('chat-history');
const queryInput = document.getElementById('query-input');
const sendButton = document.getElementById('send-button');

uploadButton.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file to upload.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            appendMessage('Assistant', `File processed successfully. Embedding ID: ${data.embedding_id}`);
        } else {
            appendMessage('Assistant', 'Error processing file.');
        }
    } catch (error) {
        console.error('Error:', error);
        appendMessage('Assistant', 'An error occurred while processing the file.');
    }
});

sendButton.addEventListener('click', async () => {
    const query = queryInput.value;
    if (!query) {
        return;
    }

    appendMessage('You', query);
    queryInput.value = '';

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        if (response.ok) {
            const data = await response.json();
            appendMessage('Assistant', data.response);
        } else {
            appendMessage('Assistant', 'Error generating response.');
        }
    } catch (error) {
        console.error('Error:', error);
        appendMessage('Assistant', 'An error occurred while generating the response.');
    }
});

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}
