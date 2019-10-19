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
        cSrCol: false,
        cCol: false,
        compareCol: false,
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
            styleObject: {backgroundColor: '#440'},
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
            products: [{}],
            searchQuery: '',
            // must provide object structure template to use {{object.name}}
            selectedRow: {name: ''},

            product_name: null,
            product_name_response: {},

            product_field: "name",
            product_value: "",
            product_edit_response: {},
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
            this.product_name_response = {};
            axios.post('/pnew', {name: this.product_name})
                .then(response => {
                    this.product_name_response = response.data;
                    this.p()
                })
                .catch(error => console.log(error));

        },

        pdelete: function () {
            this.product_name_response = {};
            axios.post('/pdelete', {name: this.product_name})
                .then(response => {
                    this.product_name_response = response.data;
                    this.p()
                }).catch(error => console.log(error));
        },

        pedit: function () {
            this.product_edit_response = {};
            axios.post('/pedit', {
                name: this.product_edit,
                field: this.product_field,
                value: this.product_value
            })
                .then(response => {
                    this.product_edit_response = response.data;
                    this.p()
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

            attributeField: ["version_number", "status"],
            gridColumns: ["id", "product_name", "version_number", "status"],

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
            this.server_response = {};
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
            this.server_response = {};
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
            this.sr_selected_response = {};
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
            this.sr_copy_response = {};
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
            recipe_json: {"Loading": "Recipe_JSON"},

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
            destination: "",
            add_response: {},


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

        sr_status: function () {
            return this.recipe_json.status
        }

    },

    methods: {
        cli_recipe: function () {
            axios.post('/cli_recipe', {
                product_name: this.$route.params.product_name,
                version_number: this.$route.params.version_number
            })
                .then(response => {
                    this.recipe_json = response.data;
                })
                .catch(error => console.log(error));
        },


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
            if (this.sr_status === "Released") {
                this.add_response = {name: 'Cannot edit "Released"'};
            } else {
                axios.post('/sr_add_c', {
                    product_name: this.$route.params.product_name,
                    version_number: this.$route.params.version_number,
                    name: this.selectedRow2.name,
                    version: this.selectedRow2.version,
                    destination: this.destination
                })
                    .then(response => {
                        this.add_response = response.data;
                        this.cli_recipe();
                        this.sr_c();
                    })
                    .catch(error => console.log(error));
            }
        },

        sr_remove_c: function () {
            this.delete_response = {};
            if (this.sr_status === "Released") {
                this.delete_response = {name: 'Cannot edit "Released"'};
            } else {
                axios.post('/sr_remove_c', {
                    product_name: this.$route.params.product_name,
                    version_number: this.$route.params.version_number,
                    name: this.selectedRow.name,
                    version: this.selectedRow.version,
                    destination: this.selectedRow.destination
                })
                    .then(response => {
                        this.delete_response = response.data;
                        this.cli_recipe();
                        this.sr_c();
                    })
                    .catch(error => console.log(error));
            }

        },

    },

    mounted: function () {
        this.cli_recipe();
        this.sr_c();
        this.c();
    },

};

const SRCompare = {
    template: '#sr-compare-template',

    data() {
        return {
            // table 1
            components1: [{}],
            gridColumns: ["name", "version", "destination"],
            searchQuery: '',


            // table 2
            components2: [{}],
            gridColumns2: ["name", "version", "destination"],
            searchQuery2: '',


            // table 3 Both
            components_both: [{}],
            gridColumns3: ["name", "version", "destination"],
            searchQuery3: '',
        }
    },

    computed: {},

    methods: {
        sr_compare: function () {
            axios.post('/sr_compare', {
                product_name: this.$route.params.product_name,
                version_number: this.$route.params.version_number,
                product_name2: this.$route.params.product_name2,
                version_number2: this.$route.params.version_number2,
            })
                .then(response => {
                    this.components1 = response.data['sr1only'];
                    this.components2 = response.data['sr2only'];
                    this.components_both = response.data['srboth'];
                })
                .catch(error => console.log(error));
        },

    },

    mounted: function () {
        this.sr_compare();
    },

};

const Components = {
    template: '#components-template',

    data: function () {
        return {
            components: [{}],
            gridColumns: ['id', 'name', 'version'],
            searchQuery: '',
        };
    },

    computed: {
        gridData: function () {
            return this.components
        },
    },

    methods: {
        c: function () {
            axios.get('/c')
                .then(response => (this.components = response.data))
                .catch(error => console.log(error));
        },
    },

    mounted: function () {
        this.c()
    },
};

const ComponentSR = {
    template: '#component-sr-template',

    data: function () {
        return {
            c_sr_list: [{}],
            gridColumns: ['id', 'product_name', 'version_number', 'status'],
            searchQuery: '',
        };
    },

    computed: {
        gridData: function () {
            return this.c_sr_list
        },
    },
    methods: {
        c_sr: function () {
            axios.post('/c_sr',
                {
                    id: this.$route.params.id,
                })
                .then(response => (this.c_sr_list = response.data))
                .catch(error => console.log(error));
        },
    },

    mounted: function () {
        this.c_sr()
    },

};

const routes = [
    {path: '/', component: Home},
    {path: '/p', component: Products},
    {path: '/sr', component: SoftwareReleases},
    {path: '/sr/:product_name/:version_number', component: SRComponents},
    {path: '/sr/compare/:product_name/:version_number/:product_name2/:version_number2', component: SRCompare},
    {path: '/c', component: Components},
    {path: '/c/:id', component: ComponentSR},
];

const router = new VueRouter({
    routes
});

const app = new Vue({
    router
}).$mount('#app');
