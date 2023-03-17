console.log("Sham Don | Top Coder 🤘🏿💀🤘🏿")


document.querySelector('#room-name-input').focus();
document.querySelector('#room-name-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#room-name-submit').click();
    }
};

document.querySelector('#room-name-submit').onclick = function (e) {
    e.preventDefault();
    var roomName = document.querySelector('#room-name-input').value;
    var slug = '';

    let tempName = roomName.toLowerCase()
    for (let index = 0; index < roomName.length; index++) {

        // slug = roomName.replace(' ', '-').toLowerCase()
        if (tempName[index] == ' ') {
            slug += '-'
        } else {
            slug += tempName[index]
        }


    }

    // 
    console.log(slug)
    window.location.pathname = '/chat/' + slug + '/';
    // window.location.reload()

};
