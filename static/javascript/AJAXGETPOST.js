function AJAXGET(url, callbackFunction) {
    let xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            callbackFunction(this);
        }
    };
    xmlHttpRequest.open("GET", url);
    xmlHttpRequest.send()
}

function AJAXGETJSON(url, callbackFunction) {
    let xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            callbackFunction(JSON.parse(this.responseText));
        }
    };
    xmlHttpRequest.open("GET", url);
    xmlHttpRequest.send()
}


function AJAXPOST(url, contentData, callbackFunction) {
    let xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            callbackFunction(this);
        }
    };
    xmlHttpRequest.open("POST", url);
    xmlHttpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlHttpRequest.send(contentData)
}


function AJAXPOSTasJSON(url, contentJSON, callbackFunction) {
    let xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            callbackFunction(this);
        }
    };
    xmlHttpRequest.open("POST", url);
    xmlHttpRequest.setRequestHeader('Content-Type', 'application/json');
    // xmlHttpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); // this will result in %22 encodings
    xmlHttpRequest.send(contentJSON)
}



function AJAXPOSTJSON(url, contentJSON, callbackFunction) {
    let xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            callbackFunction(JSON.parse(this.responseText));
        }
    };
    xmlHttpRequest.open("POST", url);
    xmlHttpRequest.setRequestHeader('Content-Type', 'application/json');
    xmlHttpRequest.send(contentJSON)
}
