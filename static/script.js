var body = document.body;
body.addEventListener('keypress', (event) => {
    if(event.key === 'w') {
        console.log('Move forward');
    }
    else if(event.key === 'a') {
        console.log('Move left');
    }
    else if(event.key === 's') {
        console.log('Move back');
    }
    else if(event.key === 'd') {
        console.log('Move right');
    }
    else {
        console.log('Stop');
    }
})