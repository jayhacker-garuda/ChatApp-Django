console.log("Sham Don | Top Coder 🤘🏿💀🤘🏿")


const MessageTypes = {
    WentOnline: 1,
    WentOffline: 2,
    TextMessage: 3,
    FileMessage: 4,
    IsTyping: 5,
    MessageRead: 6,
    ErrorOccurred: 7,
    MessageIdCreated: 8,
    NewUnreadCount: 9,
    TypingStopped: 10,
}
function getCurrentURL() {
    return window.location.href
}
const url = getCurrentURL()

const temp = url.split('/')
// console.log(MessageTypes)
const userName = JSON.parse(document.getElementById('user-name').textContent);
let chatLog = document.querySelector("#private-chat-log");

const chatSocket = new WebSocket('ws://' + location.host + '/ws/private_chat/')


function showToast(m_type, message, user, secs = 5000) {
    let alertNow = document.querySelector("#private_alert");
    // Show the toast
    // document.getElementById("private_alert").classList.remove("hidden");
    alertNow.classList.remove("hidden");
    // Hide the toast after 5 seconds (5000ms)
    // you can set a shorter/longer time by replacing "5000" with another number
    switch (m_type) {
        case 1:
            // console.log(m_type, message)
            alertNow.innerHTML = `
            <div class="flex rounded-md p-4 bg-green-100 text-green-500">
                <div  class="flex">
                    <div class="flex-shrink-0">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-green-400">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.348 14.651a3.75 3.75 0 010-5.303m5.304 0a3.75 3.75 0 010 5.303m-7.425 2.122a6.75 6.75 0 010-9.546m9.546 0a6.75 6.75 0 010 9.546M5.106 18.894c-3.808-3.808-3.808-9.98 0-13.789m13.788 0c3.808 3.808 3.808 9.981 0 13.79M12 12h.008v.007H12V12zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                        </svg>

                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-green-800">user ${user} ${message}</p>
                    </div>
                    <div class="ml-auto pl-3">
                        <div class="-mx-1.5 -my-1.5">
                            <button x-ref="button" type="button" @click="open = !open"
                            class="inline-flex bg-red-50 rounded-md p-1.5 text-red-500 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-red-50 focus:ring-red-600">
                                <span class="sr-only">Dismiss</span>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>

                            </button>
                        </div>
                    </div>
                </div>
            </div>`
            break;
        case 2:
            alertNow.innerHTML += `<div class="flex rounded-md p-4 bg-gray-100 text-gray-500">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg xmlns = "http://www.w3.org/2000/svg" fill = "none" viewBox = "0 0 24 24" stroke-width="1.5" stroke = "currentColor" class="w-6 h-6 text-gray-400" >
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3 3l8.735 8.735m0 0a.374.374 0 11.53.53m-.53-.53l.53.53m0 0L21 21M14.652 9.348a3.75 3.75 0 010 5.304m2.121-7.425a6.75 6.75 0 010 9.546m2.121-11.667c3.808 3.807 3.808 9.98 0 13.788m-9.546-4.242a3.733 3.733 0 01-1.06-2.122m-1.061 4.243a6.75 6.75 0 01-1.625-6.929m-.496 9.05c-3.068-3.067-3.664-7.67-1.79-11.334M12 12h.008v.008H12V12z" />
                        </svg>

                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-green-800">user ${user} ${message}</p>
                    </div>
                    <div class="ml-auto pl-3">
                        <div class="-mx-1.5 -my-1.5">
                            <button x-ref="button" type="button" @click="open = !open"
                            class="inline-flex bg-red-50 rounded-md p-1.5 text-red-500 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-red-50 focus:ring-red-600">
                                <span class="sr-only">Dismiss</span>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>

                            </button>
                    </div>
                </div>
            </div>
            </div>`

            break;
        case 3:

            break;
        case 4:

            break;
        case 5:
            alertNow.innerHTML += `<div class="flex rounded-md p-4 bg-gray-100 text-gray-500">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-[#fd913c]">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
                        </svg>


                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-green-800">user ${user} ${message}</p>
                    </div>
                    <div class="ml-auto pl-3">
                        <div class="-mx-1.5 -my-1.5">
                            <button x-ref="button" type="button" @click="open = !open"
                            class="inline-flex bg-red-50 rounded-md p-1.5 text-red-500 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-red-50 focus:ring-red-600">
                                <span class="sr-only">Dismiss</span>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>

                            </button>
                    </div>
                </div>
            </div>
            </div>`
            break;
        case 6:

            break;
        case 7:

            break;
        case 8:

            break;
        case 9:

            break;
        case 10:
            alertNow.innerHTML += `<div class="flex rounded-md p-4 bg-gray-100 text-gray-500">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-[#fd913c]">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
                        </svg>


                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-green-800">user ${user} ${message}</p>
                    </div>
                    <div class="ml-auto pl-3">
                        <div class="-mx-1.5 -my-1.5">
                            <button x-ref="button" type="button" @click="open = !open"
                            class="inline-flex bg-red-50 rounded-md p-1.5 text-red-500 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-red-50 focus:ring-red-600">
                                <span class="sr-only">Dismiss</span>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>

                            </button>
                    </div>
                </div>
            </div>
            </div>`

            break;

        default:
            console.error("Unknown message type!!")
            break;


    }
    setTimeout(function () {
        // document.getElementById("private_alert").classList.add("hidden");
        alertNow.classList.add("hidden");
        alertNow.innerHTML = '<div></div>'
    }, secs);
}


chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    console.log(data);

    switch (data.msg_type) {
        case 1:
            showToast(data.msg_type, data.message, data.user_pk, 8000)
            break;
        case 2:
            showToast(data.msg_type, data.message, data.user_pk)

            break;
        case 3:
            chatLog.innerHTML += 
            `
                ${data.sender == JSON.stringify(userName) ? `
                ${JSON.stringify(userName)}
                    <div class="flex justify-end mb-2">
                            <div class="rounded py-2 px-3" style="background-color: #E2F7CB">
                                <p class="text-sm mt-1">
                                    ${data.text}
                                </p>
                                <p class="text-right text-xs text-grey-dark mt-1">
                                    12:45 pm
                                </p>
                            </div>
                        </div>
                ` : `
                    <div class="flex mb-2">
                            <div class="rounded py-2 px-3" style="background-color: #F2F2F2">
                                <p class="text-sm text-purple">
                                    ${data.sender_username}
                                </p>
                                <p class="text-sm mt-1">
                                    ${data.text}
                                </p>
                                <p class="text-right text-xs text-grey-dark mt-1">
                                    12:45 pm
                                </p>
                            </div>
                        </div>
                `}
            `;
            break;
        case 4:

            break;
        case 5:
            showToast(data.msg_type, data.message, data.user_pk)
            break;
        case 6:

            break;
        case 7:

            break;
        case 8:

            break;
        case 9:

            break;
        case 10:
            showToast(data.msg_type, data.message, data.user_pk)
            break;

        default:
            break;
    }
}


// onclose - An event listener to be called when the connection is closed.
chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#private-chat-message-input').focus()

const in_Focus = document.querySelector('#private-chat-message-input');


in_Focus.addEventListener('focus', e => {
    // console.log(e.target)
    chatSocket.send(JSON.stringify({
        'msg_type': MessageTypes.IsTyping,

    }));
})


const elem = document.activeElement;
// console.log(in_Focus === elem)

// if (in_Focus === elem) {
//     chatSocket.send(JSON.stringify({
//         'msg_type': MessageTypes.IsTyping,

//     }));
// }

document.querySelector('#private-chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#private-chat-message-submit').click();
    }
};
// console.log(temp)
document.querySelector('#private-chat-message-submit').onclick = function (e) {
    // e.preventDefault();
    const messageInputDom = document.querySelector('#private-chat-message-input');

    const message = messageInputDom.value;
    var val = Math.floor(1000 + Math.random() * 9000);

    // if (elem === messageInputDom)
    //     console.log("match");
    // Send the msg object as a JSON-formatted string.
    // console.log("match");
    chatSocket.send(JSON.stringify({
        'msg_type': MessageTypes.TextMessage,
        'text': message,
        'user_pk': temp[6],
        "random_id": -val
    }));

    chatSocket.send(JSON.stringify({
        'msg_type': MessageTypes.TypingStopped,

    }));


    // Blank the text input element, ready to receive the next line of text from the user.
    messageInputDom.value = '';
};