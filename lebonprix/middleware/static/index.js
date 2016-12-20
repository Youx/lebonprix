Vue.component('dropdown', {
	template:
`<select @input="$emit('input', $event.target.value)" :value="value">
	<option v-for="elem in elements">{{ elem }}</option>
</select>`,
	props: ['elements', 'value'],
	watch: {
		elements: function(val, oldval) {
			this.$emit('input', val[0]); /* when elements change, reset selection to element 0 */
		}
	}
});

Vue.component('car-best-price', {
	template:
`<div>
	<p>Kilometrage : <input v-model='mileage' id="mileage"></input></p>
	<p>Professional : <input type="checkbox" v-model="company_ad"></input></p>
	<p>Année : <input v-model="regdate"></input></p>
	<p>{{fuel.name}} : <dropdown v-model='fuel.selected' :name="fuel.name" :elements="fuel.elements"></dropdown></p>
	<p>{{brand.name}} : <dropdown v-model='brand.selected' :name="brand.name" :elements="brand.elements"></dropdown></p>
	<p>{{model.name}} : <dropdown v-model='model.selected' :name="model.name" :elements="model.elements[brand.selected]"></dropdown></p>
	<p>{{gearbox.name}} : <dropdown v-model='gearbox.selected' :name='gearbox.name' :elements='gearbox.elements'></dropdown></p>
	<p>Detail : <input type='text' v-model='spec' placeholder='Enter spec here'></input></p>
	<button @click="predict">Predict</button>
	<div>{{result_str}}</div>
</div>
`,
	data: function() {
		return {
			spec: '',
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
				elements: {},
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
				return 'Pas assez de résultats. Prix estimé à ' + this.prediction + '€';
			} else if (this.sample_size > 200) {
				return 'Recherche trop imprécise. Prix estimé à ' + this.prediction + '€';
			} else {
				return 'Prix estimé à ' + this.prediction + '€';
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
			$.getJSON('/api/cars/params/fuel').done(function(val) {
				component.fuel.elements = val;
				component.fuel.selected = val[0];
			});
		},
		brand_model_fetch: function() {
			component = this;
			$.getJSON('/api/cars/params/brand_model').done(function(val) {
				component.brand.elements = Object.keys(val);
				component.brand.selected = component.brand.elements[0];
				component.model.elements = val;
				component.model.selected = component.model.elements[component.brand.selected][0];
			});
		},
		gearbox_fetch: function() {
			component = this;
			$.getJSON('/api/cars/params/gearbox').done(function(val) {
				component.gearbox.elements = val;
				component.gearbox.selected = val[0];
			});
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
			};
			$.ajax({
				type: 'POST',
				url: '/api/cars/predict',
				data: JSON.stringify(data),
				contentType: 'application/json'
			}).done(function(val) {
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
