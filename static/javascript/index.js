/*
use selected for picking product. #Dynamic options
https://vuejs.org/v2/guide/forms.html


https://vuejs.org/v2/examples/grid-component.html


Reusable Component for
Components list
SR list for csr

*/

// https://vuejs.org/v2/examples/grid-component.html
Vue.component('table-grid', {
    template: '#table-grid-template',
    props: {
        rows: Array,
        columns: Array,
        filterKey: String,

        // To enable eg. v-bind:detail-col="true"
        selectCol: false,
        cVerCol: false,
        cSrCol: false,
        cCol: false,
        highlighted: false, // for sr_c
    },
    data: function () {
        let sortOrders = {};
        this.columns.forEach(function (key) {
            sortOrders[key] = 1
        });
        return {
            sortKey: '',
            sortOrders: sortOrders,

            selected_row: {},
            styleObject: {
                backgroundColor: '#440'

            },
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


const Home = {template: '#home-template'};

const Products = {
    template: '#products-template',

    data() {
        return {
            products: [{}, {}],

            product_name: null,
            product_name_response: {},

            product_field: "name",
            product_value: "",
            product_edit_response: {},


            searchQuery: '',
            // must provide object structure template to use {{object.name}}
            selectedRow: {name: ''},

        }
    },

    computed: {
        gridData: function () {
            return this.products
        },
        gridColumns: function () {
            let col = [];
            for (const key in this.products[0]) {
                col.push(key)
            }
            return col
        },
        product_edit: function () {
            return this.selectedRow.name
        }
    },

    methods: {

        p: function () {
            axios.get('/p')
                .then(response => (this.products = response.data))
                .catch(error => console.log(error));
        },


        pnew: function () {
            axios.post('/pnew', {name: this.product_name})
                .then(response => {
                    this.product_name_response = response.data;
                    this.pname()
                })
                .catch(error => console.log(error));

        },

        pdelete: function () {
            axios.post('/pdelete', {name: this.product_name})
                .then(response => {
                    this.product_name_response = response.data;
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
        this.p()
    },

};

const SoftwareReleases = {
    template: '#software-releases-template',

    data() {
        return {
            software_releases: [{}],
            products: [],

            product_name: "", // selects one from product_names list
            version_number: "",
            server_response: {},

            sr_field: "",
            sr_value: "",
            sr_selected_response: {},

            version_number_new: "",
            sr_copy_response: {},

            gridColumns: ["product_name", "version_number", "status"],

            searchQuery: '',
            selectedRow: {name: ''},

        }
    },

    computed: {
        gridData: function () {
            return this.software_releases
        },
        sr_selected: function () {
            // return {
            //     product_name: this.selectedRow.product_name,
            //     version_number: this.selectedRow.version_number,
            // }
            if (this.selectedRow.product_name) {
                return (this.selectedRow.product_name + " v" + this.selectedRow.version_number)
            }
        },

        product_names: function () {
            let plist = []
            for (let i = 0; i < this.products.length; i++) {
                plist.push(this.products[i].name)
            }
            return plist
        }


    },

    methods: {
        p: function () {
            axios.get('/p')
                .then(response => (this.products = response.data))
                .catch(error => console.log(error));
        },

        sr: function () {
            axios.get('/sr')
                .then(response => (this.software_releases = response.data))
                .catch(error => console.log(error));
        },


        srnew: function () {
            axios.post('/srnew', {
                product_name: this.product_name,
                version_number: this.version_number
            })
                .then(response => {
                    this.server_response = response.data;
                    this.sr();
                })
                .catch(error => console.log(error));

        },

        srdelete: function () {
            axios.post('/srdelete', {
                product_name: this.product_name,
                version_number: this.version_number
            })
                .then(response => {
                    this.server_response = response.data;
                    this.sr()
                }).catch(error => console.log(error));
        },

        sredit: function () {
            if (this.selectedRow.status === "Released") {
                this.sr_selected_response = {name: 'Cannot edit "Released"'};
            } else {
                axios.post('/sredit', {
                    product_name: this.selectedRow.product_name,
                    version_number: this.selectedRow.version_number,
                    field: this.sr_field,
                    value: this.sr_value
                })
                    .then(response => {
                        this.sr_selected_response = response.data;
                        this.sr()
                    }).catch(error => console.log(error));
            }
        },

        sr_copy: function () {
            axios.post('/sr_copy', {
                product_name: this.selectedRow.product_name,
                version_number: this.selectedRow.version_number,
                version_number_new: this.version_number_new
            })
                .then(response => {
                    this.sr_copy_response = response.data;
                    this.sr();
                })
                .catch(error => console.log(error));

        }

    },

    mounted: function () {
        this.sr();
        this.p()

    },

};

const SRComponents = {
    template: '#sr-components-template',

    data() {
        return {

            // v-bind:style="(styleCondition ? styleObject: {})"
            sr_components: [{}],
            gridColumns: ["name", "version", "destination", "newest_version"],
            searchQuery: '',
            selectedRow: {name: ''},

            // delete
            delete_response: {},


            // table 2
            components_all: [{}],
            gridColumns2: ["name", "version"],
            searchQuery2: '',
            selectedRow2: {name: ''},

            // add
            destination: ".",
            add_response: {},


            // highlight. Compare with sr components
            cmax: [{}],

            styleCondition: false,

        }
    },

    computed: {
        sr_selected: function () {
            if (this.selectedRow.name) {
                return (this.selectedRow.name + " v" + this.selectedRow.version + " " + this.selectedRow.destination)
            }
        },

        c_selected: function () {
            if (this.selectedRow2.name) {
                return (this.selectedRow2.name + " v" + this.selectedRow2.version)
            }
        },
    },

    methods: {
        // previously /sr_c
        sr_c: function () {
            axios.post('/sr_c_highlight', {
                product_name: this.$route.params.product_name,
                version_number: this.$route.params.version_number
            })
                .then(response => {
                    this.sr_components = response.data;
                })
                .catch(error => console.log(error));
        },

        c: function () {
            axios.get('/c')
                .then(response => (this.components_all = response.data))
                .catch(error => console.log(error));
        },


        sr_add_c: function () {
            this.add_response = {};
            axios.post('/sr_add_c', {
                product_name: this.$route.params.product_name,
                version_number: this.$route.params.version_number,
                name: this.selectedRow2.name,
                version: this.selectedRow2.version,
                destination: this.destination
            })
                .then(response => {
                    this.add_response = response.data;
                    this.sr_c();
                })
                .catch(error => console.log(error));

        },

        sr_remove_c: function () {
            this.delete_response = {};
            axios.post('/sr_remove_c', {
                product_name: this.$route.params.product_name,
                version_number: this.$route.params.version_number,
                name: this.selectedRow.name,
                version: this.selectedRow.version,
                destination: this.selectedRow.destination
            })
                .then(response => {
                    this.delete_response = response.data;
                    this.sr_c();
                })
                .catch(error => console.log(error));

        },

        cmax: function () {
            axios.get('/cmax')
                .then(response => (this.cmax = response.data))
                .catch(error => console.log(error));
        },

    },

    mounted: function () {
        this.sr_c();
        this.c();
        this.cmax()
    },

};

const Components = {
    template: '#components-template',

    data: function () {
        return {
            component_highest: [{}],

            gridColumns: ['name', 'version'],
            searchQuery: '',
            // selectedRow: {name: '', version: ''},

        };
    },

    computed: {
        gridData: function () {
            return this.component_highest
        },
    },

    methods: {
        c_high: function () {
            axios.get('/cmax')
                .then(response => (this.component_highest = response.data))
                .catch(error => console.log(error));
        },
    },

    mounted: function () {
        this.c_high()
    },

};

const ComponentVersion = {
    template: '#component-version-template',

    data: function () {
        return {
            component_versions: [],

            gridColumns: ['name', 'version'],
            searchQuery: '',

        };
    },

    computed: {
        gridData: function () {
            return this.component_versions
        },
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

};

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
    {path: '/sr/:product_name/:version_number', component: SRComponents},
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



