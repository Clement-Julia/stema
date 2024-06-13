document.addEventListener("DOMContentLoaded", function() {
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + conversationId + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const chatLog = document.querySelector('#chat-log');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(data.sender_id === userId ? 'self' : 'other');
        messageElement.innerHTML = `
            <div class="message-content">${data.message}</div>
            <div class="message-timestamp">${new Date().toLocaleTimeString()}</div>
        `;
        chatLog.appendChild(messageElement);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // Enter key
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
            'sender_id': userId
        }));
        messageInputDom.value = '';
    };
});
