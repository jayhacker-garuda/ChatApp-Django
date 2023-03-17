console.log("Sham Don | Top Coder 🤘🏿💀🤘🏿")


const roomName = JSON.parse(document.getElementById('room-name').textContent);
const userName = JSON.parse(document.getElementById('user-name').textContent);

let chatLog = document.querySelector("#chat-log");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

console.log(location.host);

const chatSocket = new WebSocket('ws://' + location.host + '/ws/chat/' + roomName + '/');

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    // if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("div");
    // newOption.value = value;
    newOption.innerHTML = `
        
        <a href="http://${location.host}/private-chat/${userName}/${value}/" class="block border-b-2">
            <div class="border-l-2 border-blue-500 p-2">
                <div class="flex flex-row items-center space-x-2">
                 <img src="https://ui-avatars.com/api/?name=${value}&background=random" class="object-cover h-8 w-8 rounded-full"
                            alt="" />
                <strong class="tex-sm flex-grow">${value}</strong>
                </div>
                
            </div>
        </a>
    `;
    onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}


// onmessage - An event listener to be called when a message is received from the server.
chatSocket.onmessage = function (e) {
    // JSON.parse() converts the JSON object back into the original object,
    // then examine and act upon its contents.
    const data = JSON.parse(e.data);
    console.log(data);
    // document.querySelector('#chat-log').value += (data.username + ':\n' + data.message + '\n');
    // document.querySelector('#chat-log').value += 
    switch (data.type) {
        case "chat_message":
            chatLog.innerHTML += `
                ${data.username == userName ? `
                 <div class="flex flex-row-reverse space-x-2 space-x-reverse">
                        <img src="https://ui-avatars.com/api/?name=${data.username}&background=random" class="object-cover h-8 w-8 rounded-full"
                            alt="" />
                        
                      
                       <div class="flex flex-col">
                            <div class="p-5 bg-blue-200 rounded">
                                ${data.message}
                            </div>
                               
                            <div class="text-sm text-gray-600">2mins ago</div>
                        </div>
                    </div>
                
                `: `
                
                    <div class="flex flex-row space-x-2">
                        <img src="https://ui-avatars.com/api/?name=${data.username}&background=random" class="object-cover h-8 w-8 rounded-full"
                            alt="" />

                        <div class="flex flex-row justify-items-center">

                            <div class="flex flex-col">
                                <div class="rounded bg-gray-200 p-5">
                                    ${data.message}
                                </div>
                                <div class="text-sm text-gray-600">2mins ago</div>
                            </div>
                        </div>
                    </div>
                `}
                
                `;
            break;
        case "user_list":
            for (let i = 0; i < data.users.length; i++) {
                onlineUsersSelectorAdd(data.users[i]);
            }
            break;
        case "user_join":
            // chatLog.innerHTML += data.user + " joined the room.\n";
            chatLog.innerHTML += `
                <div class="flex flex-row justify-center text-sm text-gray-600">${data.user} joined the room</div>
            `;
            onlineUsersSelectorAdd(data.user);
            break;
        case "user_leave":
            chatLog.innerHTML += `
                <div class="flex flex-row justify-center text-sm text-gray-600">${data.user} left the room</div>
            `;
            onlineUsersSelectorRemove(data.user);
            break;
        default:
            console.error("Unknown message type!!")
            break;
    }
    // scroll 'chatLog' to the bottom
    chatLog.scrollTop = chatLog.scrollHeight;
};

// onclose - An event listener to be called when the connection is closed.
chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    // e.preventDefault();
    // print(e)
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    // Send the msg object as a JSON-formatted string.
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName
    }));

    // Blank the text input element, ready to receive the next line of text from the user.
    messageInputDom.value = '';
};