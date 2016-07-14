//
// Draw interface
//

function drawButton(){
    makeChoiceButton=createDiv("makeChoiceButton");
    var pf = partial(makeChoiceButtonClicked,27);
    makeChoiceButton.addEventListener("click",pf);
    makeChoiceButton.innerHTML="Click Here to Submit";
    $("#mainDiv").append(makeChoiceButton);
}

function drawMatch(currentMatch){
    matchText=createDiv("matchText");
    matchText.innerHTML="Match #"+currentMatch+"  Time: <time id='timer'>0</time>"+"  Self timer: <time id='selfTimer'>0</time>";
    moveTimer("selfTimer");
    moveTimer("timer");
    $("#mainDiv").append(matchText);
}

function drawStatus(number){
    numberClicks=createDiv("numberClicks");
    numberClicks.innerHTML="There have been "+number+" clicks so far.";
    $("#mainDiv").append(numberClicks);
}

function pleaseMakeChoice(message){
  matchText=document.getElementById("matchText");
  matchText.style.color="red";
  matchText.style.fontSize="200%";
}

// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // //  Actions // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 

function makeChoiceButtonClicked(someVariable){
    var message={"type":"makeChoice","variable":someVariable};
    sendMessage(message);
}


// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // //  Messages // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 



//When you receive a message of type=TYPE_HERE then the function TYPE_HEREMessage will run

function sendParameters(message){
    window['payoffVariable']=message['payoffVariable'];
}

function updateStatus(msg){
    statusManager();
}

function reconnecting(msg){
    statusManager();
}

// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // //  Status Manager // // // // // // // // // // 
// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 


function statusManager(){
  thisStatus=window.state;
  console.log(thisStatus)
  if(thisStatus[0]==-1){
    message="Loading...";
    genericScreen(message);
  }
  else if(thisStatus["page"]=="generic"){
    clearAll();
    genericScreen(thisStatus["message"]);
  }
  else if(thisStatus["page"]=="game"){//quiz
    clearAll();
    drawButton();
    drawMatch(thisStatus['currentMatch']);
    drawStatus(thisStatus['numberClicks']);
  }
  else if(thisStatus["page"]=="postMatch"){//quiz
    clearAll();
    genericScreen("That match is over");
  }
}




