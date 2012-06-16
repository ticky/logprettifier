var eventData = [];

function callback () {
    var logObject = document.getElementById('log');
    logObject.innerHTML = "";
    for (eventID in eventData) {
        var eventItem = document.createElement('li');
        eventItem.innerHTML = "r"+eventData[eventID].changeset+" by "+eventData[eventID].author+": <strong>"+eventData[eventID].message+"</strong>";
        var eventUL = document.createElement('ul');
        for (fileID in eventData[eventID].files) {
            var fileItem = document.createElement('li');
            fileItem.innerHTML = eventData[eventID].files[fileID].file;
            eventUL.appendChild(fileItem);
        }
        eventItem.appendChild(eventUL);
        logObject.appendChild(eventItem);
    }
}

function getJSON (url) {
    var http_request = new XMLHttpRequest();
    http_request.open( "GET", url, true );
    http_request.onreadystatechange = function () {
        if ( http_request.readyState == 4 && http_request.status == 200 ) {
                eventData = /*eventData.concat(*/ JSON.parse( http_request.responseText /*)*/);
                callback();
            }
    };
    http_request.send(null);
}

function loadData () {
    getJSON("/logprettifier.py");
}

function setup () {
    document.getElementById('reloaddatabutton').onclick = loadData;
}

window.onload = setup;