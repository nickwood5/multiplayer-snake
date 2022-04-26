
var playerId = 1
const gameBoard = document.getElementById('game-board')
//var socket = new WebSocket("ws://test2-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/8080")
var id
var data

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
var socket = new WebSocket("ws://new-snake-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/" + id)

socket.onopen = function(e) {
    console.log("Connect to server")
    socket.send("c")
}


window.addEventListener('keydown', press => {
    sendInput(press)

})

function setAliveNotClickable(row, column) {
    console.log("Create node at row " + row + ", col " + column)
    const cell = document.createElement('div')
    cell.style.gridRowStart = row
    cell.style.gridColumnStart = column
    cell.id = row + "," + column
    console.log("CREATE NODE " + cell.id)
    cell.classList.add('catapillarNode')
    gameBoard.appendChild(cell)
}

function removeNode(row, column) {
    let id = row + "," + column
    console.log("REMOVE NODE " + id)
    let cell = document.getElementById(id)
    cell.remove()
}



socket.onmessage = function(message) {
    if (message.data == "s") {
        console.log("STEP")
        let keys = Object.keys(data["data"]["directions"])
        //console.log(keys)
        for (let i = 0; i < keys.length; i++) {
            //console.log(keys[i])
            //console.log(data["data"]["directions"][keys[i]])
            data["data"]["nodes"][keys[i]].unshift({"x": data["data"]["nodes"][keys[i]][0]["x"] + data["data"]["directions"][keys[i]]["x"], "y": data["data"]["nodes"][keys[i]][0]["y"] + data["data"]["directions"][keys[i]]["y"]})
            if (data["data"]["growth"][keys[i]] > 0) {
                data["data"]["growth"][keys[i]] -= 1
            } else {
                let removedNode = data["data"]["nodes"][keys[i]].pop()
                let row = parseInt(removedNode["y"])
                let col = parseInt(removedNode["x"])
                removeNode(row, col)
                console.log("Remove node row" + row + ", col " + col)
            }
            console.log(parseInt(data["data"]["nodes"][keys[i]][0]["x"]))
            let row = parseInt(data["data"]["nodes"][keys[i]][0]["y"])
            let col = parseInt(data["data"]["nodes"][keys[i]][0]["x"])
            setAliveNotClickable(row, col)
            //console.log(data["data"]["nodes"][keys[i]])
        }
    } else {
        console.log(message.data)
        let response = JSON.parse(message.data)
        console.log(response)
        console.log(Object.keys(response))
        let keys = Object.keys(response)
        if (keys[0] == "data") {
            console.log("DATA RECI")
            data = response
            let players = Object.keys(data["data"]["nodes"])
            console.log("DRAWING ALL PLAYERS")
            for (let i = 0; i < players.length; i++) {
                let nodes = data["data"]["nodes"][players[i]]
                for (let j = 0; j < nodes.length; j++) {
                    let row = parseInt(nodes[j]["y"])
                    let col = parseInt(nodes[j]["x"])
                    setAliveNotClickable(row, col)
                }
            }
        } else {
            console.log("UPDATE DIRECTIONS PACK")
            for (let i = 0; i < keys.length; i++) {
                console.log("Key " + i)
                console.log(keys[i])
                data["data"]["directions"][keys[i]] = response[keys[i]]
                console.log(data["data"]["directions"])

                data["data"]["nodes"][keys[i]].unshift({"x": data["data"]["nodes"][keys[i]][0]["x"] + data["data"]["directions"][keys[i]]["x"], "y": data["data"]["nodes"][keys[i]][0]["y"] + data["data"]["directions"][keys[i]]["y"]})
                if (data["data"]["growth"][keys[i]] > 0) {
                    data["data"]["growth"][keys[i]] -= 1
                } else {
                    let removedNode = data["data"]["nodes"][keys[i]].pop()
                    let row = parseInt(removedNode["y"])
                    let col = parseInt(removedNode["x"])
                    removeNode(row, col)
                    console.log("Remove node row" + row + ", col " + col)

                }
                console.log(parseInt(data["data"]["nodes"][keys[i]][0]["x"]))
                let row = parseInt(data["data"]["nodes"][keys[i]][0]["y"])
                let col = parseInt(data["data"]["nodes"][keys[i]][0]["x"])
                setAliveNotClickable(row, col)
            }
        }
    }
    console.log(data["data"]["nodes"])
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