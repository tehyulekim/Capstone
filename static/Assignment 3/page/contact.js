/*

*/

function clickCounter() {
    if (typeof(Storage) !== "undefined") {
        if (localStorage.clickcount) {
            localStorage.clickcount = Number(localStorage.clickcount) + 1;
        } else {
            localStorage.clickcount = 1;
        }
        document.getElementById("result").innerHTML = "You have clicked the button " + localStorage.clickcount + " time(s).";
        document.getElementById('demo').innerHTML = Date()

    } else {
        document.getElementById("result").innerHTML = "Sorry, your browser does not support web storage...";
    }
}

function localStorageClear() {
    localStorage.clear();
}

function displayURL() {
    console.log(document.URL)
    console.log(document.title)
}

function test(){
    console.log(document.getElementById("firstname").value);
    console.log(document.getElementById("lastname").value);
    console.log(document.getElementById("email").value);
    console.log(document.getElementById("phone").value);
    console.log(document.getElementById("address").value);
    document.getElementById("firstname").innerHTML = localStorage.getItem("firstname");
    document.getElementById("lastname").innerHTML = localStorage.getItem("lastname");
    document.getElementById("email").innerHTML = localStorage.getItem("email");
    document.getElementById("phone").innerHTML = localStorage.getItem("phone");
    document.getElementById("address").innerHTML = localStorage.getItem("address");
}

function send() {
    if (typeof(Storage) !== "undefined") {
        // Store
        localStorage.setItem("firstname", document.getElementById("firstname").value);
        localStorage.setItem("lastname", document.getElementById("lastname").value);
        localStorage.setItem("email", document.getElementById("email").value);
        localStorage.setItem("phone", document.getElementById("phone").value);
        localStorage.setItem("address", document.getElementById("address").value);
        localStorage.setItem("date", Date());


    } else {
        document.getElementById("name").innerHTML = "Sorry, your browser does not support Web Storage...";
    }
}

function load(){

    if (typeof(Storage) !== "undefined") {
        // Retrieve
        document.getElementById("firstname").innerHTML = localStorage.getItem("firstname");
        document.getElementById("lastname").innerHTML = localStorage.getItem("lastname");
        document.getElementById("email").innerHTML = localStorage.getItem("email");
        document.getElementById("phone").innerHTML = localStorage.getItem("phone");
        document.getElementById("address").innerHTML = localStorage.getItem("address");
        document.getElementById("date").innerHTML = localStorage.getItem("date");

    } else {
        document.getElementById("name").innerHTML = "Sorry, your browser does not support Web Storage...";
    }

}