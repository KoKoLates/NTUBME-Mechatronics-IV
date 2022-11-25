document.body.addEventListener('keypress', (event) => {
    console.log(event.key);
    changeIcon(event.key);
    const request = new XMLHttpRequest();
    request.open('POST', `/ProcessUserinfo/${JSON.stringify(event.key)}`);
    request.send();
})

function changeIcon(key) {
    if(key === 'q') {
        console.log('q icon');
    }
}