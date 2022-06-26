
var playerId = 1
//var socket = new WebSocket("ws://test2-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/8080")
var id
var data
var api_url 
var app_url
var socket
var previous_direction = "u"
var gameBoard

var local_host = true

if (local_host) {
    api_url = "http://localhost:8769/get/"
    app_url = "ws://127.0.0.1:8770/"
} else {
    api_url = "http://api-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/get/"
    app_url = "ws://app-nickwood5-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com/"
}


console.log("Initializing...")

var request = new XMLHttpRequest();
request.open('GET', api_url, false);  // `false` makes the request synchronous
request.send(null);

if (request.status === 200) {
    json_response = JSON.parse(request.responseText)
    console.log(json_response.id)
    id = json_response.id
}
gameBoard = document.getElementById('game-board')
socket = new WebSocket(app_url + id)
socket.onopen = function(e) {
    console.log("Connect to server")
    socket.send("c")
}
setAliveNotClickable(1, 1, "catapillarNode")

console.log(data)



function doSomething() {
    console.log("Hey")
    console.log("Connect to server")
    socket.send("a")
    var popup = document.getElementById("myPopup");
        popup.classList.toggle("hide");

}


window.addEventListener('keydown', press => {
    sendInput(press)

})

function setAliveNotClickable(row, column, tile) {
    //console.log("Create node at row " + row + ", col " + column)
    const cell = document.createElement('div')
    cell.style.gridRowStart = row
    cell.style.gridColumnStart = column
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
    console.log(message.data)
    if (message.data[0] == "s") {
        console.log(data)
        console.log(direction)
        console.log(message.data)
        string_message = String(message.data)
        string_index = parseInt(string_message.substring(1))
        //console.log(string_index)
        previousIndex = currentIndex
        currentIndex = string_index
        console.log("Current index is " + currentIndex + " prev is " + previousIndex)


        //console.log("STEP")
        
        let keys = Object.keys(data["data"]["directions"])
        //console.log(keys)
        for (let i = 0; i < keys.length; i++) {
            //console.log("Current first node is " + data["data"]["nodes"][keys[i]][0]["x"] + ", " + data["data"]["nodes"][keys[i]][0]["y"])
            //console.log(keys[i])
            //console.log(data["data"]["directions"][keys[i]])
            //console.log("MOVING THE SNAKE!")
            data["data"]["nodes"][keys[i]].unshift({"x": data["data"]["nodes"][keys[i]][0]["x"] + data["data"]["directions"][keys[i]]["x"], "y": data["data"]["nodes"][keys[i]][0]["y"] + data["data"]["directions"][keys[i]]["y"]})
            if (data["data"]["growth"][keys[i]] > 0) {
                data["data"]["growth"][keys[i]] -= 1
            } else {
                let removedNode = data["data"]["nodes"][keys[i]].pop()
                let row = parseInt(removedNode["y"])
                let col = parseInt(removedNode["x"])
                removeNode(row, col)
                //console.log("Remove node row" + row + ", col " + col)
            }
            //console.log(parseInt(data["data"]["nodes"][keys[i]][0]["x"]))
            let row = parseInt(data["data"]["nodes"][keys[i]][0]["y"])
            let col = parseInt(data["data"]["nodes"][keys[i]][0]["x"])
            setAliveNotClickable(row, col, 'catapillarNode')
            //console.log(data["data"]["nodes"][keys[i]])
        }
    } else {

        console.log("DATA is " + message.data)
        let response = JSON.parse(message.data)
        previousIndex = currentIndex
        currentIndex = response["index"]
        //console.log(Object.keys(response))
        console.log("Current index is " + currentIndex + " prev is " + previousIndex)
        if (currentIndex != previousIndex + 1) {
            console.log("ERROR MISALIGN")
        }
        //console.log(response)
        //console.log(Object.keys(response))
        let keys = Object.keys(response)
        if (keys[0] == "data") {
            //console.log("DATA RECI")
            data = response
            let players = Object.keys(data["data"]["nodes"])
            //console.log("DRAWING ALL PLAYERS")
            for (let i = 0; i < players.length; i++) {
                let nodes = data["data"]["nodes"][players[i]]
                //console.log("Head of player " + players[i] + " at " + nodes[0]["y"] + ", " + nodes[0]["x"])
                for (let j = 0; j < nodes.length; j++) {
                    let row = parseInt(nodes[j]["y"])
                    let col = parseInt(nodes[j]["x"])
                    setAliveNotClickable(row, col, 'catapillarNode')
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
                //onsole.log("UPDATE DIRECTIONS PACK")
                let keys = Object.keys(response["movements"])

                for (let i = 0; i < keys.length; i++) {
                    data["data"]["directions"][keys[i]] = response["movements"][keys[i]]
                    //console.log(data["data"]["directions"])

                    
                }
            }
            if (Object.keys(response["new_users"]).length > 0) {
                console.log("new user")
                console.log("ID is " + id)
                let new_users = Object.keys(response["new_users"])
                for (let i = 0; i < new_users.length; i++) {
                    //if (new_users[i] != "/" + id.toString()) {
                        let nodes = response["new_users"][new_users[i]]["nodes"]
                        let growth = response["new_users"][new_users[i]]["growth"]
                        direction = response["new_users"][new_users[i]]["direction"]
                        for (let n = 0; n < nodes.length; n++) {
                            let row = parseInt(nodes[n]["y"])
                            let col = parseInt(nodes[n]["x"])
                            setAliveNotClickable(row, col, 'catapillarNode')
                        }
                        data["data"]["nodes"][new_users[i]] = nodes
                        data["data"]["growth"][new_users[i]] = growth
                        data["data"]["directions"][new_users[i]] = direction
                    //}
                }
            }
            if (Object.keys(response["dead_clients"]).length > 0) {
                //console.log("SOME CLIENTS DIED")
                let dead_clients = response["dead_clients"]
                //console.log(dead_clients)
                for (let i = 0; i < dead_clients.length; i++) {
                    let dead_client = dead_clients[i]
                    delete data["data"]["directions"][dead_client]
                    let dead_client_nodes = data["data"]["nodes"][dead_client]
                    for (let n = 0; n < dead_client_nodes.length; n++) {
                        let row = parseInt(dead_client_nodes[n]["y"])
                        let col = parseInt(dead_client_nodes[n]["x"])
                        
                        removeNode(row, col)
                        //console.log("Remove " + row + ", " + col)
                    }
                }
            }
            if (Object.keys(response["growth"]).length > 0) {
                console.log("THE SNAKE GREW")
                //console.log(response["growth"])
                let growth = response["growth"]
                let growth_keys = Object.keys(growth)
                for (let i = 0; i < growth_keys.length; i++) {
                    let grown_user = growth_keys[i]
                    let change = growth[grown_user]
                    //console.log("CURRENT GROWTH IS " + Object.keys(data["data"]["growth"]))
                    data["data"]["growth"][grown_user] += change
                    //console.log(data["data"]["growth"][grown_user])
                }
            }
            if (Object.keys(response["new_fruits"]).length > 0) {
                //console.log("SOME CLIENTS DIED")
                let new_fruits = response["new_fruits"]
                //console.log(dead_clients)
                for (let i = 0; i < new_fruits.length; i++) {
                    let new_fruit = new_fruits[i]
                    let row = new_fruit["y"]
                    let col = new_fruit["x"]
                    console.log("TRY TO ADD FRUIT " + row + ", " + col)
                    setAliveNotClickable(row, col, 'fruitPiece')
                    //delete data["data"]["directions"][dead_client]
                }
            }
            if (Object.keys(response["eaten_fruits"]).length > 0) {
                let eaten_fruits = response["eaten_fruits"]
                for (let i = 0; i < eaten_fruits.length; i++) {
                    let eaten_fruit = eaten_fruits[i]
                    let row = eaten_fruit["y"]
                    let col = eaten_fruit["x"]
                    console.log("TRY TO REMOVE FRUIT " + row + ", " + col)
                    removeNode(row, col)
                }
            }
            let keys = Object.keys(data["data"]["directions"])
            //console.log(keys)
            for (let i = 0; i < keys.length; i++) {
                //console.log("Current first node is " + data["data"]["nodes"][keys[i]][0]["x"] + ", " + data["data"]["nodes"][keys[i]][0]["y"])
                //console.log(keys[i])
                //console.log(data["data"]["directions"][keys[i]])
                //console.log("MOVING THE SNAKE!")
                data["data"]["nodes"][keys[i]].unshift({"x": data["data"]["nodes"][keys[i]][0]["x"] + data["data"]["directions"][keys[i]]["x"], "y": data["data"]["nodes"][keys[i]][0]["y"] + data["data"]["directions"][keys[i]]["y"]})
                if (data["data"]["growth"][keys[i]] > 0) {
                    data["data"]["growth"][keys[i]] -= 1
                } else {
                    let removedNode = data["data"]["nodes"][keys[i]].pop()
                    let row = parseInt(removedNode["y"])
                    let col = parseInt(removedNode["x"])
                    removeNode(row, col)
                    //console.log("Remove node row" + row + ", col " + col)
                }
                //console.log(parseInt(data["data"]["nodes"][keys[i]][0]["x"]))
                let row = parseInt(data["data"]["nodes"][keys[i]][0]["y"])
                let col = parseInt(data["data"]["nodes"][keys[i]][0]["x"])
                setAliveNotClickable(row, col, 'catapillarNode')
                //console.log(data["data"]["nodes"][keys[i]])
            }
        }
    }
    //console.log(data["data"]["nodes"])
};
  

function sendInput(press) {
    let validInput = false
    switch (press.key) {
        case "ArrowUp":
            //console.log("u")
            direction = "u"
            validInput = true
            break
        case "ArrowDown":
            //console.log("d")
            direction = "d"
            validInput = true
            break
        case "ArrowLeft":
            //console.log("l")
            direction = "l"
            validInput = true
            break
        case "ArrowRight":
            //console.log("r")
            direction = "r"
            validInput = true
            break
    }
    if (direction) {
        if (direction == "u" && previous_direction != "u" && previous_direction != "d") {
            socket.send(direction);
            previous_direction = direction
        } else if (direction == "d" && previous_direction != "u" && previous_direction != "d") {
            socket.send(direction);
            previous_direction = direction
        } else if (direction == "l" && previous_direction != "l" && previous_direction != "r") {
            socket.send(direction);
            previous_direction = direction
        } else if (direction == "r" && previous_direction != "l" && previous_direction != "r") {
            socket.send(direction); 
            previous_direction = direction
        }

    }
    //console.log(Date.now())
}

