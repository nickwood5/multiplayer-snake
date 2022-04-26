
var playerId = 1

//var socket = new WebSocket("ws://test2-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/8080")
var id

async function getJSON(url) {
    const response = await fetch(url);
    console.log(response)
    return response.json(); // get JSON from the response 
}

await getJSON("http://multiplayer-snake-api22-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/get/").then((response) => {
    console.log(response)
    id = response['id'].toString()
    console.log(id)
});

//var socket = new WebSocket("ws://127.0.0.1:8764/" + id)
var socket = new WebSocket("ws://multiplayer-snake-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com//" + id)


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
    socket.send(direction);
    
}