const APP_ID = 'c46f544d669e47d6b08d3f39f7d7418a';
const TOKEN = sessionStorage.getItem('token');
const CHANNEL = sessionStorage.getItem('room');
let UID = sessionStorage.getItem('UID');
let NAME = sessionStorage.getItem('name');

const client = AgoraRTC.createClient({mode: 'rtc', codec: 'vp8'});

let localTracks = [];
let remoteUsers = {};

// Join and Display Local Stream
let joinAndDisplayLocalStream = async () => {
    try {
        document.getElementById('room-name').innerText = CHANNEL;

        client.on('user-published', handleUserJoined);
        client.on('user-left', handleUserLeft);

        UID = await client.join(APP_ID, CHANNEL, TOKEN, UID);
        localTracks = await AgoraRTC.createMicrophoneAndCameraTracks();

        let member = await createMember();
        let player = `<div class="video-container" id="user-container-${UID}">
                        <div class="video-player" id="user-${UID}"></div>
                        <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                      </div>`;

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player);
        localTracks[1].play(`user-${UID}`);
        await client.publish([localTracks[0], localTracks[1]]);
    } catch (error) {
        console.error(error);
        window.open('/', '_self');
    }
};

// Handle when a user joins
let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user;
    await client.subscribe(user, mediaType);

    if (mediaType === 'video') {
        let player = document.getElementById(`user-container-${user.uid}`);
        if (player != null) {
            player.remove();
        }

        let member = await getMember(user);
        player = `<div class="video-container" id="user-container-${user.uid}">
                    <div class="video-player" id="user-${user.uid}"></div>
                    <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                  </div>`;
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player);
        user.videoTrack.play(`user-${user.uid}`);
    }

    if (mediaType === 'audio') {
        user.audioTrack.play();
    }
};

// Handle when a user leaves
let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid];
    document.getElementById(`user-container-${user.uid}`).remove();
};

// Leave and remove local stream
let leaveAndRemoveLocalStream = async () => {
    for (let i = 0; localTracks.length > i; i++) {
        localTracks[i].stop();
        localTracks[i].close();
    }

    await client.leave();
    deleteMember();
    window.open('/', '_self');
};

// Toggle Camera
let toggleCamera = async (e) => {
    if (localTracks[1].muted) {
        await localTracks[1].setMuted(false);
        e.target.style.backgroundColor = '#fff';
    } else {
        await localTracks[1].setMuted(true);
        e.target.style.backgroundColor = 'rgb(255, 80, 80)';
    }
};

// Toggle Mic
let toggleMic = async (e) => {
    if (localTracks[0].muted) {
        await localTracks[0].setMuted(false);
        e.target.style.backgroundColor = '#fff';
    } else {
        await localTracks[0].setMuted(true);
        e.target.style.backgroundColor = 'rgb(255, 80, 80)';
    }
};

// Create a new member
let createMember = async () => {
    let response = await fetch('/create_member/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'name': NAME, 'room_name': CHANNEL, 'UID': UID})
    });
    let member = await response.json();
    return member;
};

// Get member details
let getMember = async (user) => {
    let response = await fetch(`/get_member/?UID=${user.uid}&room_name=${CHANNEL}`);
    let member = await response.json();
    return member;
};

// Delete a member
let deleteMember = async () => {
    await fetch('/delete_member/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'name': NAME, 'room_name': CHANNEL, 'UID': UID})
    });
};

window.addEventListener("beforeunload", deleteMember);
joinAndDisplayLocalStream();

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream);
document.getElementById('camera-btn').addEventListener('click', toggleCamera);
document.getElementById('mic-btn').addEventListener('click', toggleMic);


function displayMessage(messageData) {
    const messageContainer = document.getElementById("message-container");
    const newMessage = document.createElement("div");
    newMessage.innerText = messageData.text;  // Use messageData.text to display the actual message
    messageContainer.appendChild(newMessage);
}
websocket.onmessage = function(event) {
    const messageData = JSON.parse(event.data);  // Ensure the message is properly parsed
    displayMessage(messageData);                 // Display the message when received
};
const messageText = document.getElementById('message-input').value;
const messageData = {text: messageText};  // The structure of messageData should be consistent
websocket.send(JSON.stringify(messageData));   // Send the message


const websocket = new WebSocket('ws://your-websocket-url');

// Ensure WebSocket connection is established
websocket.onopen = function() {
    console.log("WebSocket connection established");
};

// Send message when button is clicked
document.getElementById('send-button').addEventListener('click', function() {
    const messageInput = document.getElementById('message-input');
    const messageText = messageInput.value;

    // Check if the input is not empty
    if (messageText.trim() === '') {
        alert("Message cannot be empty");
        return;
    }

    const messageData = { text: messageText };

    // Send the message via WebSocket
    websocket.send(JSON.stringify(messageData));
    messageInput.value = '';  // Clear input after sending
});

// Handle incoming messages
websocket.onmessage = function(event) {
    const messageData = JSON.parse(event.data);
    displayMessage(messageData);
};

// Function to display messages
function displayMessage(messageData) {
    const messageContainer = document.getElementById("message-container");
    const newMessage = document.createElement("div");
    newMessage.innerText = messageData.text;  // Ensure this is the correct property
    messageContainer.appendChild(newMessage);
}
console.log("Sending message:", messageData);
console.log("Received message:", messageData);
websocket.onerror = function(error) {
    console.error("WebSocket error observed:", error);
};

