
var playerId = 1

window.addEventListener('keydown', press => {
    sendInput(press)

})

var socket = new WebSocket("ws://multiplayer-snake2-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/:8080")

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