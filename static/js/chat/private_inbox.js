console.log("Sham Don | Top Coder 🤘🏿💀🤘🏿")

const userName = JSON.parse(document.getElementById('user-name').textContent);


const chatSocket = new WebSocket('ws://' + location.host + '/ws/private_chat/')