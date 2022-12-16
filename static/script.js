/**
* Date: 2022-12-08
* Author: Po-Ting Ko 
*/

let grabbed = false;
let complemented = false;

/**
* Event Listener for listen to the key down events
* Send the key values to the backend and execute corresponding movements
*/
document.body.addEventListener('keydown', (event) => {
    changeKeyImages(event.key);
    const request = new XMLHttpRequest();
    request.open('POST', `/ProcessUserinfo/${JSON.stringify(event.key)}`);
    request.send();
})

/**
* Event Listener for listen to the key up events
* Send the stop command to backend and let the robot stop after previous command
*/
document.body.addEventListener('keyup', (event) => {
    document.getElementById("move").src="/static/images/default.png";
    if(event.key === 'ArrowUp' || event.key === 'ArrowLeft' || 
        event.key === 'ArrowDown' || event.key === 'ArrowRight') {
        const request = new XMLHttpRequest();
        request.open('POST', `/ProcessUserinfo/${JSON.stringify('Stop')}`);
        request.send();
    }
})

/**
* Corresponding to the key, change the style or effetcs
* @param key the event key of the keyboard being preesed
*/
function changeKeyImages(key/*str*/) {
    let plus = document.getElementById("plus");
    let move = document.getElementById("move");
    let comp = document.getElementById("complemented");
    let plusText = document.getElementById("plus_text");
    if(key === 'ArrowUp') {
        move.src="/static/images/up.png";
    }
    else if(key === 'ArrowLeft') {
        move.src="/static/images/left.png";
    }
    else if(key === 'ArrowDown') {
        move.src="/static/images/down.png";
    }
    else if(key === 'ArrowRight') {
        move.src="/static/images/right.png";
    }
    else if(key === '+') {
        // Change into indicate icon, and set the flag in opposite 
        grabbed ? ((plus.src="/static/images/release.png"), 
                    grabbed = false, 
                    plusText.textContent = "RELEASE") :
                  ((plus.src="/static/images/grab.png"), 
                    grabbed = true, 
                    plusText.textContent = "GRABBED");
    }
    else if(key === 'c' || key === 'C') {
        // Change into indicate icon, and set the flag in opposite 
        complemented ? ((comp.src="/static/images/sunUnpress.png"), complemented = false) :
        ((comp.src="/static/images/sunPress.png"), complemented = true);
    }
}

/**
* Recieve the info sending from backend and divide into different function 
* to execuate corresponding mission.
*/
function recieveSendInfo() {
    fetch('/ProcessSendinfo').then((response) => {
        response.json().then((data) => {
            changeTempText(data['TEMP']);
            distanceTo(data['DISTL'], data['DISTR']);
        }) 
    });
}

/**
* The function to change the word content of temperature
* @param tempText the string text of current temperature
*/
function changeTempText(tempText/*str*/) {
    let text = document.getElementById("temperature_text");
    tempText == "" ? text.innerHTML = "--" : text.innerHTML = tempText + " &degC";
}

/**
* Accorsing to the distance data sending from the backend side.
* The function try to execuate indicate mission on icon, text and warning.
* @param left the left side distance
* @param right the right side distance
*/
function distanceTo(left/*str*/, right/*str*/) {
    var leftDist = parseInt(left);
    var rightDist = parseInt(right);
    let carImg = document.getElementById("car_image");
    let carText = document.getElementById("car_text");
    // As well as the robot near by the obstacles, then shown the warning icon
    if(leftDist <= 25) {
        (rightDist <= 25) ? (carImg.src="/static/images/carBoth.png") :
        (carImg.src="/static/images/carLeft.png");
    }
    else {
        (rightDist <= 25) ? (carImg.src="/static/images/carRight.png") :
        (carImg.src="/static/images/carDefault.png");
    }

    // change the string text formate.
    if(leftDist < 10) {
        (rightDist < 10) ? carText.textContent = `0${leftDist} cm || 0${rightDist} cm` :
        carText.textContent = `0${leftDist} cm || ${rightDist} cm`;
    }
    else {
        (rightDist < 10) ? carText.textContent = `${leftDist} cm || 0${rightDist} cm` :
        carText.textContent = `${leftDist} cm || ${rightDist} cm`;
    }
}

// set the interval timer to repeatly call recieve function.
setInterval(recieveSendInfo, 500);
