console.log("Sham Don | Top Coder 🤘🏿💀🤘🏿")


const roomName = JSON.parse(document.getElementById('room-name').textContent);
const userName = JSON.parse(document.getElementById('user-name').textContent);
let chatLog = document.querySelector("#private-chat-log");

function getCurrentURL() {
    return window.location.href
}
const url = getCurrentURL()

const temp = url.split('/')

function return_name(user, other_user) {
    if (user == other_user)
        return temp[4];

    return user
}
// ---0------1--------2------------------3-------------4----------------5------6--
// ["http:", "", "127.0.0.1:8000", "private-chat", "vewalij884", "jayhacker", ""]
// console.log(temp)

const chatSocket = new WebSocket('ws://' + location.host + '/ws/private-chat/' + return_name(userName, temp[5]) + '/' + temp[5] + '/');


chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    console.log(data);


    switch (data.type) {
        case "private_chat_message":
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
        case "user_join_private_chat":
            // chatLog.innerHTML += data.user + " joined the room.\n";
            chatLog.innerHTML += `
                <div class="flex flex-row justify-center text-sm text-gray-600">${data.user} joined the private-room</div>
            `;
            break;
        case "user_leave_private_chat":
            chatLog.innerHTML += `
                <div class="flex flex-row justify-center text-sm text-gray-600">${data.user} left the private-room</div>
            `;
            break;
        default:
            console.error("Unknown message type!!")
            break;
    }

    // scroll 'chatLog' to the bottom
    chatLog.scrollTop = chatLog.scrollHeight;
}

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};


document.querySelector('#private-chat-message-input').focus();
document.querySelector('#private-chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#private-chat-message-submit').click();
    }
};

document.querySelector('#private-chat-message-submit').onclick = function (e) {
    // e.preventDefault();
    // print(e)
    const messageInputDom = document.querySelector('#private-chat-message-input');
    const message = messageInputDom.value;
    // Send the msg object as a JSON-formatted string.
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName
    }));

    // Blank the text input element, ready to receive the next line of text from the user.
    messageInputDom.value = '';
};
