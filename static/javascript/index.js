/*
use selected for picking product. Dynamic options
https://vuejs.org/v2/guide/forms.html


*/

Vue.component('blog-post', {
    props: ['title'],
    template: '<h4>{{ title }}</h4>'
});


Vue.component('products-list', {
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
`
});

// 1. Define route components. These can be imported from other files
const Home = {template: `<div><h1>Software Component Store and Release Assembly Tools</h1></div>`};

const Products = {
    data() {
        return {
            product_names: [],
            product_new: null,
            product_new_response: null,

            product_selected: null,
            product_edit: null,
            product_delete: null,

            picked: null,
            selected: null,

            data1: "data1old",

        }
    },
    methods: {
        newProduct: function () {
            axios.post('/pnew',
                {
                    product_name: this.product_new,
                })
                .then(response => (this.product_new_response = response.data))
                .catch(error => console.log(error));
        },

        func1: function () {

            axios.post('/5', {
                firstName: 'fp1firstname',
                lastName: 'fp1lastname'
            })
                .then(response => (this.data1 = response.data))
                .catch(error => console.log(error));
            // this.data1 = "data1new"
        }


    },


    mounted: function () {
        axios.get('/pname')
            .then(response => (this.product_names = response.data))
            .catch(error => console.log(error));
    },

    template: `
<div>
<h1>Products Page</h1>
<hr/>
<h1> {{ product_names }} </h1>
<hr/>
<input v-model="product_new" placeholder="New Product">
<span>Message is: </span>
<p>{{ product_new }}</p>
<hr/>

<input type="radio" id="one" value="One" v-model="picked">
<label for="one">One</label>
<br>
<input type="radio" id="two" value="Two" v-model="picked">
<label for="two">Two</label>
<br>
<span>Picked: {{ picked }}</span>

<hr/>
<button v-on:click="func1">Func1 Button</button>
<span>data1 is : {{data1}}</span>


    
    
</div>`
};

const Foo = {
    data: function () {
        return {
            message1: null,
            message2: null,
            posts: []
        };
    },

    methods: {
        say: function () {
            axios.get('https://jsonplaceholder.typicode.com/posts')
                .then((response) => {
                    this.posts = response.data
                });
        },
    },

    mounted: function () {

        // http://127.0.0.1:5000/b, fixes origin policy
        axios.get('/b')
            .then(response => (this.message1 = response.data))
            .catch(error => console.log(error));

        axios.post('/8', {
            firstName: 'fp1firstname',
            lastName: 'fp1lastname'
        })
            .then(response => (this.message2 = response.data))
            .catch(error => console.log(error));

        this.say()
    },

    template: `<div>
    <span>message1: {{ message1 }}</span>
    <hr/>
    <span>message2: {{ message2 }}</span>
    <hr/>
    <blog-post
      v-for="post in posts"
      v-bind:key="post.id"
      v-bind:title="post.title"
    ></blog-post>
</div>`
};


const Bar = {
    data: function () {
        return {
            data1: 1,
            data2: 2
        };

    },

    methods: {
        say: function (message) {
            alert(message)
        },

    },


    mounted: function () {

        axios.get('/b')
            .then(response => (this.data1 = response.data))
            .catch(error => console.log(error));

        axios.post('/5',
            {
                x: '1',
                y: '2'
            })
            .then(response => (this.data2 = response.data))
            .catch(error => console.log(error));

    },

    template: `<div>
  <button v-on:click="say('hi')">Say hi</button>
</div>`
};

const Page1 = {
    data: function () {
        return {
            message: 'hello vue',
            products: [
                {name: "product1", property: "property1"},
                {name: "product2", property: "property1"},
                {name: "product3", property: "property1"},
            ],
            component_names: [],
            name: "app1 name",
            data1: "data1text",
        }
    },
    methods: {
        post5: function () {
            axios.post('/5',
                {
                    firstName: '123',
                    lastName: '123213'
                })
                .then(response => this.data1 = response.data)

        },

        func1: function () {
            axios.post('/5', {
                firstName: 'fp1firstname',
                lastName: 'fp1lastname'
            })
                .then(response => (this.data1 = response.data))
                .catch(error => console.log(error));
            // this.data1 = "data1new"
        }
    },

    mounted: function () {
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

        axios.get('/cname')
            .then(function (response) {
                this.component_names = response.data.component_names;
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });


    },


    template: `
<div>     
      <section>
        <h1>Section heading</h1>
        <hr/>
        <button v-on:click="post5">Post5 Button</button>
        <span>data1 is : {{data1}}</span>
        
        <button v-on:click="func1">Func1 Button</button>
        <span>data1 is : {{data1}}</span>

        <hr/>

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

        force reload CTRL click

        <h1 v-if="true">true</h1>
        <h1 v-else>false</h1>


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

// 4. Create and mount the root instance. inject the router with the router option to make the whole app router-aware.
const app = new Vue({
    router
}).$mount('#app');



