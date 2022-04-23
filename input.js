
var playerId = 1

window.addEventListener('keydown', press => {
    sendInput(press)

})

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
    let socket = new WebSocket("ws://100.65.191.217:8765")

    socket.onopen = function(e) {
    socket.send(playerId.toString() + ":" + direction);
    };
}