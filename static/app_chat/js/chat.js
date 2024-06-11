document.addEventListener("DOMContentLoaded", function() {
    var chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/');

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        document.querySelector('#chat-messages').innerHTML += '<div>' + data.message + '</div>';
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    window.sendMessage = function() {
        var messageInputDom = document.querySelector('#message-input');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };
});













// // Assurez-vous que l'URL de la WebSocket correspond à celle définie dans votre routing.py
// var chatSocket = new WebSocket(
//     'ws://' + window.location.host.replace("8000", "8001") + '/ws/chat/'
// );

// chatSocket.onmessage = function(e) {
//     var data = JSON.parse(e.data);
//     document.querySelector('#chat-log').value += (data.message + '\n');
// };

// chatSocket.onclose = function(e) {
//     console.error('Chat socket closed unexpectedly');
// };

// document.querySelector('#chat-message-input').focus();
// document.querySelector('#chat-message-input').onkeyup = function(e) {
//     if (e.keyCode === 13) {  // Touche "Enter"
//         document.querySelector('#chat-message-submit').click();
//     }
// };

// document.querySelector('#chat-message-submit').onclick = function(e) {
//     var messageInputDom = document.querySelector('#chat-message-input');
//     var message = messageInputDom.value;
//     chatSocket.send(JSON.stringify({
//         'message': message
//     }));
//     messageInputDom.value = '';
// };
