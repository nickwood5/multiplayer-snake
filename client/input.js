
var playerId = 1
//var socket = new WebSocket("ws://test2-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/8080")
var id
var data
var api_url 
var app_url
var socket
var previous_direction = "u"
var gameBoard
var speed_up = false

var local_host = false

if (local_host) {
    api_url = "http://localhost:8769/get/"
    app_url = "ws://127.0.0.1:8770/"
} else {
    api_url = "https://nickwood5.pythonanywhere.com/get/"
    app_url = "wss://websockets-echo-nick.herokuapp.com/"
}




//console.log("Initializing...")

var request = new XMLHttpRequest();
request.open('GET', api_url, false);  // `false` makes the request synchronous
request.send(null);

if (request.status === 200) {
    json_response = JSON.parse(request.responseText)
    //console.log(json_response.id)
    id = json_response.id
}
gameBoard = document.getElementById('game-board')
socket = new WebSocket(app_url + id)
socket.onopen = function(e) {
    //console.log("Connect to server")
    let connect_json = {"type": "connect"}
    let connect_packet = JSON.stringify(connect_json)
    socket.send(connect_packet)
}

function random_colour() {
    var random_colour = "#" + Math.floor(Math.random()*16777215).toString(16);
    return random_colour
}

document.getElementById('colorPicker').value = random_colour();

function doSomething() {
    //console.log("Hey")
    //console.log("Connect to server")
    
    var popup = document.getElementById("myPopup");
    var colorPicker = document.getElementById("colorPicker")
    var playerColor = colorPicker.value

    let spawn_json = {"type": "spawn", "colour": playerColor}
    let spawn_packet = JSON.stringify(spawn_json)

    socket.send(spawn_packet)
    //console.log(playerColor)
    popup.classList.toggle("hide");

}


window.addEventListener('keydown', press => {
    sendInput(press)

})

window.addEventListener('keyup', press => {
    keyUp(press)
})


function setAliveNotClickable(row, column, tile, colour) {
    //console.log("color is " + colour)
    //console.log("Create node at row " + row + ", col " + column)
    const cell = document.createElement('div')
    cell.style.gridRowStart = row
    cell.style.gridColumnStart = column
    cell.style.setProperty("--node-color", colour)
    cell.id = row + "," + column
    //console.log("CREATE NODE " + cell.id)
    cell.classList.add(tile)
    gameBoard.appendChild(cell)
}



function removeNode(row, column) {
    let id = row + "," + column
    //console.log("REMOVE NODE " + id)
    let cell = document.getElementById(id)
    cell.remove()
}

var currentIndex = 0
var previousIndex = 0
var string_index
var string_message
var direction

socket.onmessage = function(message) {
    console.log(Math.round((new Date()).getTime() / 1000) + " " + message.data)
    response = JSON.parse(message.data)
    
    keys = Object.keys(response)
    if (keys[0] == "data") {
        data = response
        let players = Object.keys(data["data"]["nodes"])
        for (let i = 0; i < players.length; i++) {
            let nodes = data["data"]["nodes"][players[i]]
            for (let j = 0; j < nodes.length; j++) {
                let row = parseInt(nodes[j]["y"])
                let col = parseInt(nodes[j]["x"])
                setAliveNotClickable(row, col, 'colourNode', data["data"]["colours"][players[i]])
            }
        }
        let fruits = data["data"]["fruits"]
        for (let i = 0; i < fruits.length; i++) {
            let row = parseInt(fruits[i]["y"])
            let col = parseInt(fruits[i]["x"])
            setAliveNotClickable(row, col, 'fruitPiece')
        }
    } else {
        if (Object.keys(response["movements"]).length > 0) {
            let keys = Object.keys(response["movements"])

            for (let i = 0; i < keys.length; i++) {
                data["data"]["directions"][keys[i]] = response["movements"][keys[i]]     
            }
        }
        if (Object.keys(response["new_users"]).length > 0) {
            let new_users = Object.keys(response["new_users"])
            for (let i = 0; i < new_users.length; i++) {
                    console.log("Client spawned " + new_users[i])
                    console.log(response)
                    let nodes = response["new_users"][new_users[i]]["nodes"]
                    let growth = response["new_users"][new_users[i]]["growth"]
                    let colour = response["new_users"][new_users[i]]["colours"]
                    direction = response["new_users"][new_users[i]]["direction"]
                    for (let n = 0; n < nodes.length; n++) {
                        let row = parseInt(nodes[n]["y"])
                        let col = parseInt(nodes[n]["x"])
                        setAliveNotClickable(row, col, 'colourNode', colour)
                    }
                    data["data"]["nodes"][new_users[i]] = nodes
                    data["data"]["growth"][new_users[i]] = growth
                    data["data"]["directions"][new_users[i]] = direction
                    data["data"]["colours"][new_users[i]] = colour
                //}
            }
        }
        if (Object.keys(response["dead_clients"]).length > 0) {
            let dead_clients = response["dead_clients"]
            for (let i = 0; i < dead_clients.length; i++) {
                let dead_client = dead_clients[i]
                console.log("Client " + dead_client + " died")
                console.log(response)
                delete data["data"]["directions"][dead_client]
                let dead_client_nodes = data["data"]["nodes"][dead_client]
                for (let n = 0; n < dead_client_nodes.length; n++) {
                    let row = parseInt(dead_client_nodes[n]["y"])
                    let col = parseInt(dead_client_nodes[n]["x"])
                    
                    removeNode(row, col)
                }
            }
        }
        if (Object.keys(response["growth"]).length > 0) {
            let growth = response["growth"]
            let growth_keys = Object.keys(growth)
            for (let i = 0; i < growth_keys.length; i++) {
                let grown_user = growth_keys[i]
                let change = growth[grown_user]
                data["data"]["growth"][grown_user] += change
            }
        }
        if (Object.keys(response["new_fruits"]).length > 0) {
            let new_fruits = response["new_fruits"]

            for (let i = 0; i < new_fruits.length; i++) {
                let new_fruit = new_fruits[i]
                let row = new_fruit["y"]
                let col = new_fruit["x"]
                setAliveNotClickable(row, col, 'fruitPiece')
            }
        }
        if (Object.keys(response["eaten_fruits"]).length > 0) {
            let eaten_fruits = response["eaten_fruits"]
            for (let i = 0; i < eaten_fruits.length; i++) {
                let eaten_fruit = eaten_fruits[i]
                let row = eaten_fruit["y"]
                let col = eaten_fruit["x"]

                removeNode(row, col)
            }
        }
        
    }
    if (response["user_steps"] != null) {

        previousIndex = currentIndex
        currentIndex = string_index

        let keys = response["user_steps"]

        for (let i = 0; i < keys.length; i++) {
            console.log("Trying to move snake " + keys[i])
            console.log(response)

            data["data"]["nodes"][keys[i]].unshift({"x": data["data"]["nodes"][keys[i]][0]["x"] + data["data"]["directions"][keys[i]]["x"], "y": data["data"]["nodes"][keys[i]][0]["y"] + data["data"]["directions"][keys[i]]["y"]})
            if (data["data"]["growth"][keys[i]] > 0) {
                data["data"]["growth"][keys[i]] -= 1
            } else {
                let removedNode = data["data"]["nodes"][keys[i]].pop()
                let row = parseInt(removedNode["y"])
                let col = parseInt(removedNode["x"])
                removeNode(row, col)
            }
            let row = parseInt(data["data"]["nodes"][keys[i]][0]["y"])
            let col = parseInt(data["data"]["nodes"][keys[i]][0]["x"])
            setAliveNotClickable(row, col, 'colourNode', data["data"]["colours"][keys[i]])
        }
    }
};

function keyUp(press) {
    let validInput = false
    switch (press.key) {
        case "ArrowUp":
            direction = "u"
            validInput = true
            break
        case "ArrowDown":
            direction = "d"
            validInput = true
            break
        case "ArrowLeft":
            direction = "l"
            validInput = true
            break
        case "ArrowRight":
            direction = "r"
            validInput = true
            break
    }
    if (validInput == true && speed_up == true) {
        slow_down_json = {"type": "decrease_speed"}
        slow_down_packet = JSON.stringify(slow_down_json)
        socket.send(slow_down_packet)
        speed_up = false
    }
}

function sendInput(press) {
    let validInput = false
    switch (press.key) {
        case "ArrowUp":
            direction = "u"
            validInput = true
            break
        case "ArrowDown":
            direction = "d"
            validInput = true
            break
        case "ArrowLeft":
            direction = "l"
            validInput = true
            break
        case "ArrowRight":
            direction = "r"
            validInput = true
            break
    }
    if (validInput) {
        if (direction == previous_direction && speed_up == false) {
            speed_up_json = {"type": "increase_speed"}
            speed_up_packet = JSON.stringify(speed_up_json)
            socket.send(speed_up_packet)
            speed_up = true
        } else {
            if (direction == "u" && previous_direction != "u" && previous_direction != "d") {
                move_json = {"type": "move", "direction": direction}
                move_packet = JSON.stringify(move_json)
                socket.send(move_packet);
                previous_direction = direction
            } else if (direction == "d" && previous_direction != "u" && previous_direction != "d") {
                move_json = {"type": "move", "direction": direction}
                move_packet = JSON.stringify(move_json)
                socket.send(move_packet);
                previous_direction = direction
            } else if (direction == "l" && previous_direction != "l" && previous_direction != "r") {
                move_json = {"type": "move", "direction": direction}
                move_packet = JSON.stringify(move_json)
                socket.send(move_packet);
                previous_direction = direction
            } else if (direction == "r" && previous_direction != "l" && previous_direction != "r") {
                move_json = {"type": "move", "direction": direction}
                move_packet = JSON.stringify(move_json)
                socket.send(move_packet);
                previous_direction = direction
            }
        }
    }
}