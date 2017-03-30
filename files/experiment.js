// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // //  Draw Interface // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 

function drawButton() {
    placeText({"divid":"makeChoiceButton","text":"Click Here to Submit","top":"400px","left":"700px","width":"200px","height":"100px","backgroundColor":"rgba(255,0,0,.11)"})
    clickButton("many","makeChoiceButton",makeChoiceButtonClicked,27);
}

function drawMatch(currentMatch) {
    var matchText = createAndAddDiv("matchText","mainDiv");
    var thisText = "Match #" + currentMatch + "  Time: <time id='everyoneTimer'>0</time>";
    console.log("sdfsdf",thisText);
    placeText({"divid":"matchText","text":thisText,"top":"200px","left":"600px","width":"400px","height":"100px","fontSize":"25px"});
    // moveTimer("selfTimer");
    moveTimer("everyoneTimer");
}

function drawStatus(number) {
    var thisText = "There have been " + number + " clicks so far.";
    placeText({"divid":"numberClicks","text":thisText,"top":"700px","left":"600px","width":"400px","height":"100px","fontSize":"25px"});
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
