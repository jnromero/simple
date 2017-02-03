// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // //  Draw Interface // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 

function drawButton() {
    var makeChoiceButton = createAndAddDiv("makeChoiceButton","mainDiv");
    makeChoiceButton.innerHTML = "Click Here to Submit";
    clickButton("many","makeChoiceButton",makeChoiceButtonClicked,27);
}

function drawMatch(currentMatch) {
    var matchText = createAndAddDiv("matchText","mainDiv");
    matchText.innerHTML = "Match #" + currentMatch + "  Time: <time id='timer'>0</time>" + "  Self timer: <time id='selfTimer'>0</time>";
    moveTimer("selfTimer");
    moveTimer("timer");
}

function drawStatus(number) {
    var numberClicks = createAndAddDiv("numberClicks","mainDiv");
    numberClicks.innerHTML = "There have been " + number + " clicks so far.";
}

function pleaseMakeChoice(message) {
    var matchText = document.getElementById("matchText");
    matchText.style.color = "red";
    matchText.style.fontSize = "200%";
}

// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // //  Actions // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 

function makeChoiceButtonClicked(someVariable) {
    var message = { "type": "makeChoice", "variable": someVariable };
    sendMessage(message);
}


// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // //  Messages // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 



//When you receive a message of type=TYPE_HERE then the function TYPE_HEREMessage will run

function sendParameters(message) {
    window['payoffVariable'] = message['payoffVariable'];
}


function reconnecting(msg) {
    statusManager();
}

// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // //  Status Manager // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 


function statusManager() {
    var thisStatus = window.state;
    console.log(thisStatus)
    if (thisStatus[0] == -1) {
        var message = "Loading...";
        genericScreen(message);
    } else if (thisStatus["page"] == "generic") {
        clearAll();
        genericScreen(thisStatus["message"]);
    } else if (thisStatus["page"] == "game") {
        clearAll();
        drawButton();
        drawMatch(thisStatus['currentMatch']);
        drawStatus(thisStatus['numberClicks']);
    } else if (thisStatus["page"] == "postMatch") {
        clearAll();
        genericScreen("That match is over.  The next match will start in <time id='timer'>0</time>");
    }
}
