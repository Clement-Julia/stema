// document.addEventListener("DOMContentLoaded", function() {
//     const chatSocket = new WebSocket(
//         'ws://' + window.location.host + '/ws/chat/' + conversationId + '/'
//     );

//     chatSocket.onmessage = function(e) {
//         const data = JSON.parse(e.data);
//         const chatLog = document.querySelector('#chat-log');

//         if (data.type === 'chat_message') {
//             const messageElement = document.createElement('div');
//             messageElement.classList.add('message');
//             messageElement.classList.add(data.sender_id === userId ? 'self' : 'other');
//             messageElement.innerHTML = `
//                 <div class="message-content">
//                     ${conversationParticipants.length > 2 ? `<strong>${data.sender_username}</strong><br>` : ''}
//                     ${data.message}
//                 </div>
//                 <div class="message-timestamp">${new Date().toLocaleTimeString()}</div>
//             `;
//             chatLog.appendChild(messageElement);
//             chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom
//         } else if (data.type === 'user_connected' || data.type === 'user_disconnected') {
//             const statusIndicator = document.getElementById('status-' + data.user_id);
//             if (statusIndicator) {
//                 statusIndicator.className = 'status-indicator ' + (data.type === 'user_connected' ? 'online' : 'offline');
//             }
//         }
//     };

//     chatSocket.onclose = function(e) {
//         console.error('Chat socket closed unexpectedly');
//     };

//     document.querySelector('#chat-message-input').focus();
//     document.querySelector('#chat-message-input').onkeyup = function(e) {
//         if (e.keyCode === 13) {  // Enter key
//             document.querySelector('#chat-message-submit').click();
//         }
//     };

//     document.querySelector('#chat-message-submit').onclick = function(e) {
//         const messageInputDom = document.querySelector('#chat-message-input');
//         const message = messageInputDom.value;
//         chatSocket.send(JSON.stringify({
//             'message': message,
//             'sender_id': userId
//         }));
//         messageInputDom.value = '';
//     };
// });
document.addEventListener("DOMContentLoaded", function() {
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + conversationId + '/'
    );

    chatSocket.onmessage = function(e) {
        console.log(e,'test');
        const data = JSON.parse(e.data);
        console.log(data);
        const chatLog = document.querySelector('#chat-log');

        if (data.type === 'chat_message') {
            console.log('oui');
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');
            messageElement.classList.add(data.sender_id === userId ? 'self' : 'other');
            messageElement.innerHTML = `
                <div class="message-content">
                    ${conversationParticipants.length > 2 ? `<strong>${data.sender_username}</strong><br>` : ''}
                    ${data.message}
                </div>
                <div class="message-timestamp">${new Date().toLocaleTimeString()}</div>
            `;
            chatLog.appendChild(messageElement);
            console.log('oui2')
            chatLog.scrollTop = chatLog.scrollHeight;
        } else if (data.type === 'user_connected' || data.type === 'user_disconnected') {
            const statusIndicator = document.getElementById('status-' + data.user_id);
            if (statusIndicator) {
                statusIndicator.className = 'status-indicator ' + (data.type === 'user_connected' ? 'online' : 'offline');
            }
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {
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

    // Ajouter un ami à la conversation
    document.querySelector('#add-friend-btn').onclick = function() {
        const friendSelect = document.querySelector('#friend-select');
        const friendId = friendSelect.value;

        fetch('/social/add_participants/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'conversation_id': conversationId,
                'friend_id': friendId
            })
        }).then(response => response.json())
          .then(data => {
              if (data.status === 'success') {
                  alert('Ami ajouté à la conversation');
                  location.reload();
              } else {
                  alert('Erreur lors de l\'ajout de l\'ami à la conversation');
              }
          });
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});