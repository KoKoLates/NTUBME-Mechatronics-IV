var grabbed = false;

document.body.addEventListener('keydown', (event) => {
    console.log(event.key);
    changeKeyImages(event.key);
    const request = new XMLHttpRequest();
    request.open('POST', `/ProcessUserinfo/${JSON.stringify(event.key)}`);
    request.send();
})

document.body.addEventListener('keyup', (event) => {
    document.getElementById("move").src="/static/images/default.png";
})

function changeKeyImages(key) {
    var plus = document.getElementById("plus");
    var move = document.getElementById("move");
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
        grabbed ? ((plus.src="/static/images/release.png"), grabbed = false) :
        ((plus.src="/static/images/grab.png"), grabbed = true);
    }
}

function replaceInText(text) {
    document.getElementById("temp").innerHTML=text;
}