let grabbed = false;
let complemented = false;

document.body.addEventListener('keydown', (event) => {
    changeKeyImages(event.key);
    const request = new XMLHttpRequest();
    request.open('POST', `/ProcessUserinfo/${JSON.stringify(event.key)}`);
    request.send();
})

document.body.addEventListener('keyup', (event) => {
    document.getElementById("move").src="/static/images/default.png";
    if(event.key === 'ArrowUp' || event.key === 'ArrowLeft' || 
        event.key === 'ArrowDown' || event.key === 'ArrowRight') {
        const request = new XMLHttpRequest();
        request.open('POST', `/ProcessUserinfo/${JSON.stringify('Stop')}`);
        request.send();
    }
})

function changeKeyImages(key) {
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
        grabbed ? ((plus.src="/static/images/release.png"), 
                    grabbed = false, 
                    plusText.textContent = "RELEASE") :
                  ((plus.src="/static/images/grab.png"), 
                    grabbed = true, 
                    plusText.textContent = "GRABBED");
    }
    else if(key === 'c' || key === 'C') {
        complemented ? ((comp.src="/static/images/sunUnpress.png"), complemented = false) :
        ((comp.src="/static/images/sunPress.png"), complemented = true);
    }
}

function recieveSendInfo() {
    fetch('/ProcessSendinfo').then((response) => {
        response.json().then((data) => {
            changeTempText(data['TEMP']);
            distanceTo(data['DISTL'], data['DISTR']);
        }) 
    });
}

function changeTempText(tempText) {
    let text = document.getElementById("temperature_text");
    tempText == "" ? text.innerHTML = "--" : text.innerHTML = tempText + " &degC";
}

function distanceTo(left, right) {
    var leftDist = parseInt(left);
    var rightDist = parseInt(right);
    let carImg = document.getElementById("car_image");
    let carText = document.getElementById("car_text");
    if(leftDist <= 25) {
        (rightDist <= 25) ? (carImg.src="/static/images/carBoth.png") :
        (carImg.src="/static/images/carLeft.png");
    }
    else {
        (rightDist <= 25) ? (carImg.src="/static/images/carRight.png") :
        (carImg.src="/static/images/carDefault.png");
    }

    if(leftDist < 10) {
        (rightDist < 10) ? carText.textContent = `0${leftDist} cm || 0${rightDist} cm` :
        carText.textContent = `0${leftDist} cm || ${rightDist} cm`;
    }
    else {
        (rightDist < 10) ? carText.textContent = `${leftDist} cm || 0${rightDist} cm` :
        carText.textContent = `${leftDist} cm || ${rightDist} cm`;
    }
}

setInterval(recieveSendInfo, 500);
