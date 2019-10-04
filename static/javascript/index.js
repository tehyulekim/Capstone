let app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        message: 'hello vue',
        products: [
            {name: "product1", property: "property1"},
            {name: "product2", property: "property1"},
            {name: "product3", property: "property1"},
        ],
        component_names: []
    },
    created() {
        axios.get('/cname')
            .then(function (response) {
                this.component_names = response.data.component_names
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }
});


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