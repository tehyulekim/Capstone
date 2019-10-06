/*
https://github.com/axios/axios

    axios.post('/user', {
    firstName: 'Fred',
    lastName: 'Flintstone'
})
    .then(function (response) {
        console.log(response);
    })
    .catch(function (error) {
        console.log(error);
    });

 */

// http://127.0.0.1:5000/1
function f5() {
    jsobject1 = {
        firstName: 'Fred',
        lastName: 'Flintstone'
    };
    // send jsobject without JSON.stringify()
    axios.post('/5', jsobject1)
        .then(function (response) {
            object1 = response.data; // is object, not string
            document.getElementById("id5").innerHTML = JSON.stringify(response.data);
            document.getElementById("id6").innerHTML = response.data.lastName;
            x = response; // type x.data in console
            console.log("x.data = " + x.data);
            console.log("response.data = " + response.data);
            console.log("response.data.firstName = " + response.data.firstName);
            console.log("response.data.lastName = " + response.data.lastName);
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });
}

function f6() {
    document.getElementById("id6").innerHTML = "message text";
}

function f7() {
    alert("stnd")
}


function fp1() {
    axios.post('/5', {
        firstName: 'fp1firstname',
        lastName: 'fp1lastname'
    })
        .then(function (response) {
            object1 = response.data; // is object, not string
            x = response; // type x.data in console
            // document.getElementById("p1").innerHTML = response.data.lastName;
            document.getElementById("p1").innerHTML = JSON.stringify(response.data);

        })
        .catch(function (error) {
            console.log(error);
        });

}





