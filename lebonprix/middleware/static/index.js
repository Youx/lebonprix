Vue.component('search-select', {
	template:
`<div class="form-group">
	<label>{{title}}</label>
	<select class="form-control" @input="$emit('input', $event.target.value)" :value="value">
		<option v-for="elem in elements">{{ elem }}</option>
	</select>
</div>`,
	props: ['elements', 'value', 'title'],
	watch: {
		elements: function(val, oldval) {
			this.$emit('input', val[0]); /* when elements change, reset selection to element 0 */
		}
	}
});

Vue.component('search-mileage', {
	template:
`<div class="form-group">
	<label>{{title}}</label>
	<div class="input-group">
		<input @input="$emit('input', $event.target.value)" :value='value' class="form-control"></input>
		<div class='input-group-addon'>km</div>
	</div>
</div>`,
	props: ['title', 'value']
});

Vue.component('search-company-ad', {
	template:
`<div class='form-check'>
	<label class='form-check-label'>
		<input class='form-check-input' type="checkbox" :value='value' @input="$emit('input', $event.target.value)">
		{{title}}
	</label>
</div>`,
	props: ['title', 'value']
});

Vue.component('search-text', {
	template:
`<div class="form-group">
	<label>{{title}}</label>
	<input class="form-control" type='text' :value='value' @input="$emit('input', $event.target.value)" :placeholder='placeholder'></input>
</div>
`,
	props: ['title', 'placeholder', 'value']
});

Vue.component('search-int', {
	template:
`<div class="form-group">
	<label>{{title}}</label>
	<input class="form-control" type='number' :value='value' @input="$emit('input', $event.target.value)"></input>
</div>`,
	props: ['title', 'value']
});

Vue.component('search-radio', {
	template:
`<div class="form-group">
	<div><label>{{title}}</label></div>
	<label class="form-check-label" v-for="elem in elements">
		<input type='radio' class='form-check-input' v-model='internal' :value="elem"> {{elem}}
	</label>
</div>`,
	data: function() { return { internal: '' }; },
	props: ['title', 'value', 'elements'],
	watch: {
		elements: function(val, oldval) {
			this.$emit('input', val[0]); /* when elements change, reset selection to element 0 */
		},
		internal: function(val, oldval) {
			this.$emit('input', val);
		},
		value: function(val, oldval) {
			this.internal = val;
		}
	},
});

var bus = new Vue();

Vue.component('car-best-price', {
	template:
`<div>
	<legend>Critères primaires</legend>
	<search-select v-model='brand.value' :title='brand.title' :elements="brand.elements"></search-select>
	<search-select v-model='model.value' :title='model.title' :elements="model.elements[brand.value]"></search-select>
	<search-select v-model='fuel.value' :title='fuel.title' :elements="fuel.elements"></search-select>
	<search-text v-model='spec.value' :title='spec.title' :placeholder='spec.placeholder'></search-text>

	<legend>Critères prédictifs</legend>
	<search-mileage v-model='mileage.value' :title='mileage.title'></search-mileage>
	<search-company-ad v-model='company_ad.value' :title='company_ad.title'></search-company-ad>
	<search-int v-model='regdate.value' :title='regdate.title'></search-int>
	<search-radio v-model='gearbox.value' :title='gearbox.title' :elements='gearbox.elements'></search-radio>
	<button class="btn btn-primary" @click="predict" :disabled='searching'>Predict</button>
</div>
`,
	data: function() {
		return {
			spec: {
				title: 'Détail',
				placeholder: 'Modèle/motorisation (ex: 1.6 vti, 320d, 1.6 120, ...)',
				value: ''
			},
			mileage: {
				title: 'Kilometrage',
				value: 0
			},
			company_ad: {
				title: 'Professionel',
				value: false
			},
			regdate: {
				title: 'Année',
				value: 2016
			},
			fuel: {
				title: "Carburant",
				elements: [''],
				value: ''
			},
			brand: {
				title: "Marque",
				elements: [],
				value: ''
			},
			model: {
				title: "Modele",
				elements: {},
				value: ''
			},
			gearbox: {
				name: 'Boite de vitesse',
				elements: [],
				value: ''
			},
			prediction: -1,
			sample_size: -1,
			searching: false,
		};
	},
	created: function() {
		this.fuel_fetch();
		this.brand_model_fetch();
		this.gearbox_fetch();
	},
	methods: {
		fuel_fetch: function() {
			var component = this;
			$.getJSON('/api/cars/params/fuel').done(function(val) {
				component.fuel.elements = val;
			});
		},
		brand_model_fetch: function() {
			var component = this;
			$.getJSON('/api/cars/params/brand_model').done(function(val) {
				component.brand.elements = Object.keys(val);
				component.model.elements = val;
			});
		},
		gearbox_fetch: function() {
			var component = this;
			$.getJSON('/api/cars/params/gearbox').done(function(val) {
				component.gearbox.elements = val;
			});
		},
		predict: function() {
			var component = this;
			component.searching = true;
			bus.$emit('searching', true);
			var data = {
				brand: this.brand.value,
				model: this.model.value,
				fuel: this.fuel.value,
				gearbox: this.gearbox.value,
				regdate: this.regdate.value,
				mileage: this.mileage.value,
				spec: this.spec.value,
				company_ad: this.company_ad.value
			};
			$.ajax({
				type: 'POST',
				url: '/api/cars/predict',
				data: JSON.stringify(data),
				contentType: 'application/json'
			}).done(function(val) {
				component.searching = false;
				bus.$emit('searching', false);
				bus.$emit('prediction', {
					price: val.price,
					sample_size: val.sample_size
				});
			});
		}
	}
});

Vue.component('loading', {
	template:
`<div v-if='display_on'>
	<i class="fa fa-refresh fa-spin fa-3x fa-fw" aria-hidden="true"></i>
	<span class="sr-only">Refreshing...</span>
</div>`,
	props: ['display_on']
});

Vue.component('prediction-price', {
	template:
`<div v-if='display_on'>
	<div>price : {{price}}</div>
	<div>sample size : {{sample_size}}</div>
</div>
`,
	props: ['display_on', 'price', 'sample_size']
});

Vue.component('prediction-frame', {
	template:
`<div>
	<loading :display_on='searching'></loading>
	<prediction-price :display_on='prediction.available'
					  :price='prediction.price'
					  :sample_size='prediction.sample_size'>
	</prediction-price>
</div>
`,
	data: function() {
		return {
			searching: false,
			prediction: {
				available: false,
				price: -1,
				sample_size: -1
			}
		};
	},
	created: function() {
		var component = this;
		bus.$on('prediction', function(val) {
			component.prediction.available = true;
			component.prediction.price = val.price;
			component.prediction.sample_size = val.sample_size;
		});
		bus.$on('searching', function(val) {
			component.searching = val;
			if (component.searching == true)
				component.prediction.available = false;
		});
	}
});

var app = new Vue({
	el: '#main'
});
