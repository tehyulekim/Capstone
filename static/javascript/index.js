/*
use selected for picking product. #Dynamic options
https://vuejs.org/v2/guide/forms.html


https://vuejs.org/v2/examples/grid-component.html


Reusable Component for
Components list
SR list for csr

*/

// https://vuejs.org/v2/examples/grid-component.html
Vue.component('demo-grid', {
    template: '#grid-template',
    props: {
        rows: Array,
        columns: Array,
        filterKey: String,
    },
    data: function () {
        let sortOrders = {};
        this.columns.forEach(function (key) {
            sortOrders[key] = 1
        });
        return {
            sortKey: '',
            sortOrders: sortOrders,

            selected_row: null,
        }
    },
    computed: {
        filteredRows: function () {
            let sortKey = this.sortKey;
            let filterKey = this.filterKey && this.filterKey.toLowerCase();
            let order = this.sortOrders[sortKey] || 1;
            let rows = this.rows;
            if (filterKey) {
                rows = rows.filter(function (row) {
                    return Object.keys(row).some(function (key) {
                        return String(row[key]).toLowerCase().indexOf(filterKey) > -1
                    })
                })
            }
            if (sortKey) {
                rows = rows.slice().sort(function (a, b) {
                    a = a[sortKey];
                    b = b[sortKey];
                    return (a === b ? 0 : a > b ? 1 : -1) * order
                })
            }
            return rows
        }
    },
    filters: {
        capitalize: function (str) {
            return str.charAt(0).toUpperCase() + str.slice(1)
        }
    },
    methods: {
        sortBy: function (key) {
            this.sortKey = key;
            this.sortOrders[key] = this.sortOrders[key] * -1
        }
    }
});

Vue.component('product-list', {
    props: ['name'],
    template: '<h4>{{ name }}</h4>'
});

const Home = {template: '#home-template'};

const Products = {
    data() {
        return {
            product_names: null,
            product_new: null,
            product_new_response: null,

            product_edit: null,
            product_field: "name",
            product_value: null,
            product_edit_response: null,


            product_delete: null,
            product_delete_response: null,


            product_selected: null,

        }
    },
    methods: {

        pname: function () {
            axios.get('/pname')
                .then(response => (this.product_names = response.data))
                .catch(error => console.log(error));
        },


        pnew: function () {
            axios.post('/pnew', {name: this.product_new})
                .then(response => {
                    this.product_new_response = response.data;
                    this.pname()
                })
                .catch(error => console.log(error));

        },

        pdelete: function () {
            axios.post('/pdelete', {name: this.product_delete})
                .then(response => {
                    this.product_delete_response = response.data;
                    this.pname()
                }).catch(error => console.log(error));
        },

        pedit: function () {
            axios.post('/pedit', {
                name: this.product_edit,
                field: this.product_field,
                value: this.product_value
            })
                .then(response => {
                    this.product_edit_response = response.data;
                    this.pname()
                }).catch(error => console.log(error));
        },


    },

    mounted: function () {
        this.pname()
    },

    template: '#products-template'
};

const SoftwareReleases = {
    data: function () {
        return {
            searchQuery: '',
            gridColumns: ['name', 'power'],
            gridData: [
                {name: 'Chuck Norris', power: Infinity},
                {name: 'Bruce Lee', power: 9000},
                {name: 'Jackie Chan', power: 7000},
                {name: 'Jet Li', power: 8000}
            ],

            // must provide object structure template to use {{object.name}}
            selectedRow: {name:''},

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

    template: '#software-releases-template'
};

const SRVersion = {
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

    template: '#srversion-template'
};

const SRComponent = {
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

const Components = {
    data: function () {
        return {
            component_names: null,
            component_highest: null,
        };
    },

    methods: {
        c_high: function () {
            axios.get('/c')
                .then(response => (this.component_highest = response.data))
                .catch(error => console.log(error));
        },
    },

    mounted: function () {
        this.c_high()
    },

    template: '#components-template'
};

const ComponentVersion = {
    data: function () {
        return {
            component_versions: null,
        };
    },

    methods: {
        c_versions: function () {
            axios.post('/cversion',
                {
                    name: this.$route.params.name,
                })
                .then(response => (this.component_versions = response.data))
                .catch(error => console.log(error));
        },
    },

    mounted: function () {
        this.c_versions()
    },

    template: '#component-version-template'
};

// Associated SR
const ComponentSR = {
    data: function () {
        return {
            srlist: null,
        };
    },

    methods: {
        csearchsr: function () {
            axios.post('/csearchsr',
                {
                    name: this.$route.params.name,
                    version: this.$route.params.version
                })
                .then(response => (this.srlist = response.data))
                .catch(error => console.log(error));
        },
    },


    mounted: function () {
        this.csearchsr()
    },

    template: '#component-sr-template'
};


const Foo = {
    template: '#foo-template',

    data: function () {
        return {
            message1: null,
            message2: null,
            posts: null
        };
    },

    methods: {},

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

    },

};

const Bar = {
    template: '#bar-template',

    data: function () {
        return {
            data1: 1,
        };
    },

    methods: {},

    mounted: function () {

    },
};

const Page1 = {
    template: '#page1-template',
    data: function () {
        return {
            message: 'hello vue',
            products: [
                {name: "product1", property: "property1"},
                {name: "product2", property: "property1"},
                {name: "product3", property: "property1"},
            ],
            component_names: null,
            name: "app1 name",
            data1: "data1text",
            picked: null,
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
                console.log(error);
                this.errored = true
            })
            .finally(() => this.loading = false);

        axios.get('/cname')
            .then(function (response) {
                this.component_names = response.data.component_names;
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    },


};

const Page2 = {
    template: '#page2-template',
    data: function () {
        return {
            data222: "data222text",
            data2: 2,
            ver1: this.$route.params.ver,
            component_name: this.$route.params.id,

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
};


const routes = [
    {path: '/', component: Home},
    {path: '/c', component: Components},
    {path: '/c/:name', component: ComponentVersion},
    {path: '/c/:name/:version', component: ComponentSR},
    {path: '/p', component: Products},
    {path: '/sr', component: SoftwareReleases},
    {path: '/sr/:name', component: SRVersion},
    {path: '/sr/:name/:version', component: SRComponent},
    {path: '/foo', component: Foo},
    {path: '/bar', component: Bar},
    {path: '/page1', component: Page1},
    {path: '/page2/:ver/:id', component: Page2},

];

const router = new VueRouter({
    routes // short for `routes: routes`
});

// 4. Create and mount the root instance. inject the router with the router option to make the whole app router-aware.
const app = new Vue({
    router
}).$mount('#app');



