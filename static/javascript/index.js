let BlogPost = Vue.component('blog-post', {
    props: ['title'],
    template: '<h3>{{ title }}</h3>'
})

cgreeting = Vue.component('greeting', {
    props: ['title'],
    template: `
<div>
<p>hi, I am {{ title }} </p>
<p>what is your name?</p>
</div>`,
});

ProductsList = Vue.component('products-list', {
    props: ['data2'],
    template: `
<div>
{{ data2 }}
</div>`,
});

// https://vuejs.org/v2/guide/components.html
Vue.component('button-counter', {
    data: function () {
        return {
            count: 0
        }
    },
    template: `
<button v-on:click="count++">You clicked me {{ count }} times.</button>
`,
});

// 1. Define route components. These can be imported from other files
const Products = {
    props: ['data3'],
    template: `
<div>
Products Page
        <button type="button" onclick=fp1()>Test Button 1</button>
        <div id="p1">p1</div>
        <products-list 
        v-bind:data2="data1"
        ></products-list>
        
        
        <blog-post
          v-for="post in posts"
          v-bind:key="post.id"
          v-bind:title="post.title"
        ></blog-post>

</div>`
};

const Home = {template: `<div></div>`};

const Foo = {
    template: `<div>Foo page
      <blog-post
          v-for="post in posts"
          v-bind:key="post.id"
          v-bind:title="post.title"
        ></blog-post>
</div>`
};

const Bar = {
    template: `
<div>

bar
<div id="id8">8</div>
<button v-on:click="myFunctionOnLoad()">Greet</button>


</div>`
};

const Page1 = {
    data: {
        message: 'hello vue',
        products: [
            {name: "product1", property: "property1"},
            {name: "product2", property: "property1"},
            {name: "product3", property: "property1"},
        ],
        component_names: [],
        name: "app1 name",

        data1: "data1 text message data 1",

        posts: []


    },
    methods: {
        myFunctionOnLoad: function () {
            document.getElementById("id8").innerHTML = "javascript message text element id 8";
        },

        post5: function () {
            axios.post('/5', {
                firstName: 'fp1firstname',
                lastName: 'fp1lastname'
            })
                .then(function (response) {
                    object1 = response.data; // is object, not string
                    x = response; // type x.data in console
                    // document.getElementById("p1").innerHTML = response.data.lastName;
                    // document.getElementById("p1").innerHTML = JSON.stringify(response.data);
                    this.data1 = JSON.stringify(response.data);
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
    },
    created: function () {
        // Alias the component instance as `vm`, so that we
        // can access it inside the promise function
        var vm = this
        // Fetch our array of posts from an API
        fetch('https://jsonplaceholder.typicode.com/posts')
            .then(function (response) {
                return response.json()
            })
            .then(function (data) {
                vm.posts = data
            });


        axios.get('/cname')
            .then(function (response) {
                this.component_names = response.data.component_names;
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    },

    mounted:
        function () {

            axios
                .get('https://api.coindesk.com/v1/bpi/currentprice.json')
                .then(response => {
                    this.info = response.data.bpi
                })
                .catch(error => {
                    console.log(error)
                    this.errored = true
                })
                .finally(() => this.loading = false)
        },

    template: `
<div>     
      <section>
        <h1>Section heading</h1>
        <br/>
        <button type="button" onclick="">Test Button 1</button>
        <button type="button" onclick="">Test Button 2</button>
        <button type="button" onclick="">Test Button 3</button>
        <button type="button" onclick="">Test Button 4</button>
        <button type="button" onclick=f5()>Test Button 5</button>
        <button type="button" onclick=f6()>Test Button 6</button>
        <button type="button" onclick=f7()>Test Button 7</button>

        <div id="id1">1</div>
        <div id="id2">2</div>
        <div id="id3">3</div>
        <div id="id4">4</div>
        <div id="id5">5</div>
        <div id="id6">6</div>

        <br/>

      </section>

      <section>
        <h1>Vue App</h1>
        <ul>
          <li v-for="product in products">
            {{ product }}
            {{ product.name }}
            {{ product.property}}
            {{ message }}
          </li>
        </ul>


        <label>
          <input type="text" v-model="message">
          {{ message }}
        </label>


        Component changes
        <ul>
          <li v-for="component_name in component_names">
            {{ component_name }}
          </li>
        </ul>
        {{ component_names }}

        force reload

        <greeting></greeting>


        <h1 v-if="1===2">Vue is home!</h1>
        <h1 v-else>Oh no 😢</h1>
        <h1 v-if="page==='1'">Vue is 1!</h1>
        <h1 v-if="page==='2'">Vue is 2!</h1>

        <p v-if="false">1111</p>
        <p v-else>2222</p>

        <p v-if="true">3333</p>
        <p v-else>4444</p>

        <h1 v-if="ok">Yes</h1>
        <h1 v-else>No</h1>


      </section>

      <section>
        <h1>HTML form input</h1>
        <form action="http://127.0.0.1:5000/6" method="post">
          <label>
            <input type="text" name="name1" value="v1">
            <input type="text" name="name2" value="v2">
            <input type="text" name="name3" value="v3">
            <input type="submit" value="Submit">
          </label>
        </form>

        <form onsubmit="f1()">
          <label for="text1">text1 label</label>
          <input type="text" id="text1">
        </form>


      </section>




      <button-counter></button-counter>

</div>`
};

const routes = [
    {path: '/', component: Home},
    {path: '/p', component: Products},
    {path: '/page1', component: Page1},
    {path: '/foo', component: Foo},
    {path: '/bar', component: Bar}
];

const router = new VueRouter({
    routes // short for `routes: routes`
});

// 4. Create and mount the root instance.
// Make sure to inject the router with the router option to make the whole app router-aware.
const app = new Vue({
    router
}).$mount('#app');



