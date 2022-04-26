
var playerId = 1

var socket = new WebSocket("ws://localhost:8765/3")
socket.onopen = function(e) {
    socket.send("assign_id")
}

window.addEventListener('keydown', press => {
    sendInput(press)

})

socket.onmessage = function(message) {
    console.log(message.data)
};
  

function sendInput(press) {
    let validInput = false
    let direction = "a"
    switch (press.key) {
        case "ArrowUp":
            console.log("u")
            direction = "u"
            validInput = true
            break
        case "ArrowDown":
            console.log("d")
            direction = "d"
            validInput = true
            break
        case "ArrowLeft":
            console.log("l")
            direction = "l"
            validInput = true
            break
        case "ArrowRight":
            console.log("r")
            direction = "r"
            validInput = true
            break
    }
    if (validInput) {
        console.log("Input is " + direction)
    }
    

    console.log(Date.now())
    socket.send(playerId.toString() + ":" + direction);
    
}