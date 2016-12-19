Vue.component('dropdown', {
	template: 
`<p>{{ name }}
	<select v-on:change="changed">
		<option v-for="elem in elements">{{ elem }}</option>
	</select>
</p>`,
	props: ['name', 'elements', 'value'],
	methods: {
		changed: function(event) {
			this.$emit('input', event.target.value);
		}
	}
});

Vue.component('car-best-price', {
	template:
`<form action="#">
	<p>Kilometrage <input v-model='mileage' id="mileage"></input></p>
	<p>Professional <input type="checkbox" v-model="company_ad"></input></p>
	<p>Année <input v-model="regdate"></input></p>
	<dropdown v-model='fuel.selected' :name="fuel.name" :elements="fuel.elements"></dropdown>
	<dropdown v-model='brand.selected' @input="brand_changed" :name="brand.name" :elements="brand.elements"></dropdown>
	<dropdown v-model='model.selected' :name="model.name" :elements="model.elements"></dropdown>
	<dropdown v-model='gearbox.selected' :name='gearbox.name' :elements='gearbox.elements'></dropdown>
	<p>Detail <input type='text' v-model='spec'></input></p>
	<button type="submit" @click="predict">Predict</button>
	<div>pending : {{search_pending}}, prediction {{prediction}}, sample_size {{sample_size}}</div>
</form>
`,
	data: function() {
		return {
			spec: 'Enter spec here',
			mileage: 0,
			company_ad: false,
			regdate: 2016,
			fuel: {
				name: "Carburant",
				elements: [''],
				selected: ''
			},
			brand: {
				name: "Marque",
				elements: [],
				selected: ''
			},
			model: {
				name: "Modele",
				elements: [],
				selected: ''
			},
			gearbox: {
				name: 'Boite de vitesse',
				elements: [],
				selected: ''
			},
			brand_model: {},
			prediction: -1,
			sample_size: -1,
			search_pending: false,
		};
	},
	computed: {
		result_str: function() {
			this.search_pending;
			this.prediction;
			this.sample_size;
			if (this.search_pending) {
				return 'Please wait...';
			} else if (this.prediction == -1) {
				return '';
			} else if (this.sample_size < 30) {
				return 'Pas assez de résultats. Prix estimé à {0}€'.format(this.prediction);
			} else if (this.sample_size > 200) {
				return 'Recherche trop imprécise. Prix estimé à {0}€.'.format(this.prediction);
			} else {
				return 'Prix estimé à {0}€'.format(this.prediction);
			}
		}
	},
	created: function() {
		this.fuel_fetch();
		this.brand_model_fetch();
		this.gearbox_fetch();
	},
	methods: {
		fuel_fetch: function() {
			component = this;
			fetch(
				new Request('/api/cars/params/fuel', { method: 'GET' })
			).then(function(val) {
				return val.json();
			}).then(function(val) {
				component.fuel.elements = val;
				component.fuel.selected = val[0];
			});
		},
		brand_model_fetch: function() {
			component = this;
			fetch(
				new Request('/api/cars/params/brand_model', { method: 'GET' })
			).then(function(val) {
				return val.json();
			}).then(function(val) {
				component.brand_model = val;
				component.brand.elements = Object.keys(val);
				component.brand.selected = component.brand.elements[0];
				component.model.elements = val[component.brand.selected];
				component.model.selected = component.model.elements[0]
			});
		},
		gearbox_fetch: function() {
			component = this;
			fetch(
				new Request('/api/cars/params/gearbox', { method: 'GET' })
			).then(function(val) {
				return val.json();
			}).then(function(val) {
				component.gearbox.elements = val;
				component.gearbox.selected = val[0];
			});
		},
		brand_changed: function(val) {
			this.model.elements = this.brand_model[val];
			this.model.selected = this.model.elements[0];
		},
		model_changed: function() {
			console.log("model changed");
		},
		predict: function() {
			component = this;
			this.search_pending = true;
			var data = {
				brand: this.brand.selected,
				model: this.model.selected,
				fuel: this.fuel.selected,
				gearbox: this.gearbox.selected,
				regdate: this.regdate,
				mileage: this.mileage,
				spec: this.spec,
				company_ad: this.company_ad
			}
			fetch(
				new Request('/api/cars/predict', { method: 'POST', body: JSON.stringify(data), headers: {'Content-Type': 'application/json'} })
			).then(function(val) {
				return val.json();
			}).then(function(val) {
				component.prediction = val.price;
				component.sample_size = val.sample_size;
				component.search_pending = false;
			});
		}
	}
});

var app7 = new Vue({
	el: '#main'
});