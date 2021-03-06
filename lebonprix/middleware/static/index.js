Vue.component('help-tooltip', {
	template:
`<span :id='id' class='glyphicon glyphicon-question-sign'
	   data-toggle="tooltip" data-placement="right" trigger='hover'
	   :title="text">
</span>`,
	props: ['id', 'text'],
	mounted: function() {
		$('#'+this.id).tooltip();
	}
});

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
	<h4>Critères primaires
		<help-tooltip :id='tooltips.primary_crit.id' :title='tooltips.primary_crit.title'></help-tooltip>
	</h4>
	<search-select v-model='brand.value' :title='brand.title' :elements="brand.elements"></search-select>
	<search-select v-model='model.value' :title='model.title' :elements="model.elements[brand.value]"></search-select>
	<search-select v-model='fuel.value' :title='fuel.title' :elements="fuel.elements"></search-select>
	<search-text v-model='spec.value' :title='spec.title' :placeholder='spec.placeholder'></search-text>

	<div>
		<ul class="nav nav-tabs" role="tablist">
			<li role="presentation" class="active"><a href="#car-predict" aria-controls="car-predict" role="tab" data-toggle="tab">Estimation</a></li>
			<li role="presentation"><a href="#car-bestoffers" aria-controls="car-bestoffers" role="tab" data-toggle="tab">Meilleures offres</a></li>
		</ul>

		<div class='tab-content'>
			<div role='tabpanel' class='tab-pane active' id='car-predict'>
				<h4>Critères prédictifs
					<help-tooltip :id='tooltips.predict_crit.id' :title='tooltips.predict_crit.title'></help-tooltip>
				</h4>
				<search-mileage v-model='mileage.value' :title='mileage.title'></search-mileage>
				<search-company-ad v-model='company_ad.value' :title='company_ad.title'></search-company-ad>
				<search-int v-model='regdate.value' :title='regdate.title'></search-int>
				<search-radio v-model='gearbox.value' :title='gearbox.title' :elements='gearbox.elements'></search-radio>
				<button class="btn btn-primary" @click="predict" :disabled='searching'>Estimer</button>
			</div>
			<div role='tabpanel' class='tab-pane' id='car-bestoffers'>
				<h4>Critères de choix</h4>
				<search-int v-model='max_price.value' :title='max_price.title'></search-int>
				<search-mileage v-model='max_mileage.value' :title='max_mileage.title'></search-mileage>
				<search-radio v-model='gearbox.value' :title='gearbox.title' :elements='gearbox.elements'></search-radio>
				<button class="btn btn-primary" @click="find_best_offers" :disabled='searching'>Trouver</button>
			</div>
		</div>
	</div>
</div>
`,
	data: function() {
		return {
			tooltips: {
				primary_crit: {
					id: 'primary_crit',
					title: 'Ces critères servent à filtrer des voitures existantes.'
				},
				predict_crit: {
					id: 'predict_crit',
					title: 'Ces critères servent à prédire une voiture théorique.'
				}
			},
			spec: {
				title: 'Détail',
				placeholder: 'Modèle/motorisation (ex: 1.6 vti, 320d, 1.6 120, ...)',
				value: ''
			},
			mileage: {
				title: 'Kilometrage',
				value: 0
			},
			max_mileage: {
				title: 'Kilometrage max',
				value: 0
			},
			max_price: {
				title: 'Prix maximum',
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
					sample_size: val.sample_size,
					samples: val.samples
				});
			});
		},
		find_best_offers: function() {
			var component = this;
			component.searching = true;
			bus.$emit('searching', true);
			var data = {
				brand: this.brand.value,
				model: this.model.value,
				fuel: this.fuel.value,
				gearbox: this.gearbox.value,
				max_mileage: this.max_mileage.value,
				spec: this.spec.value,
				max_price: this.max_price.value
			};
			$.ajax({
				type: 'POST',
				url: '/api/cars/best_offers',
				data: JSON.stringify(data),
				contentType: 'application/json'
			}).done(function(val) {
				component.searching = false;
				bus.$emit('searching', false);
				bus.$emit('best-offers', {
					results: val.results,
					sample_size: val.sample_size,
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
	<h2>Ca vaut probablement dans les {{rounded_price}} €</h2>
	<div>taille de l'échantillon : {{sample_size}}</div>
</div>`,
	props: ['display_on', 'price', 'sample_size'],
	computed: {
		rounded_price: function() {
			return Math.round10(this.price, 2);
		}
	}
});

Vue.component('prediction-samples', {
	template:
`<div v-if='display_on'>
	<h2>Ce genre de voiture?
		<help-tooltip :id='tooltip.id' :text='tooltip.text'></help-tooltip>
	</h2>
	<div class='row' style='display: flex;'>
		<div v-for='element in elements' class='col-sm-3' style='display: flex;'>
			<div class='thumbnail' style='width: 100%'>
				<img :src='element.picture' :alt='element.title'></img>
				<div class='caption'><h3>{{ element.title }}<h3></div>
			</div>
		</div>
	</div>
</div>`,
	data: function() {
		return {
			tooltip: {
				id: 'tooltip1',
				text: 'Pas assez précis? Remplissez le champ de recherche "Détail"'
			}
		};
	},
	props: ['elements', 'display_on'],
});

Vue.component('prediction-frame', {
	template:
`<div>
	<loading :display_on='searching'></loading>
	<prediction-samples :display_on='prediction.available'
						:elements='prediction.samples'>
	</prediction-samples>
	<prediction-price :display_on='prediction.available'
					  :price='prediction.price'
					  :sample_size='prediction.sample_size'>
	</prediction-price>
</div>`,
	data: function() {
		return {
			searching: false,
			prediction: {
				samples: [],
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
			component.prediction.samples = val.samples;
		});
		bus.$on('searching', function(val) {
			component.searching = val;
			if (component.searching == true)
				component.prediction.available = false;
		});
	}
});

Vue.component('best-offer', {
	template:
`<div class='thumbnail' style='width: 100%' :href='url'>
	<img :src='thumb' :alt='subject'></img>
	<div class='caption' style='display: flex; flex-direction: column'>
		<h4>{{ subject }}</h4>
		<div>{{ price }}€ au lieu de {{expected_price}}€ = {{economy_pc}}%</div>
		<div>{{ regdate}} / {{ mileage }}km</div>
	</div>
	<div><a class='btn btn-primary' :href='url'>Annonce</a></div>
</div>`,
	props: ['id', 'thumb', 'subject', 'price', 'expected_price', 'mileage', 'regdate', 'economy_pc'],
	computed: {
		url: function() {
			return 'http://www.leboncoin.fr/voitures/'+this.id+'.htm';
		}
	}
});

Vue.component('best-offers-frame', {
	template:
`<div v-if='best_offers.available'>
	<h2>Les meilleurs plans :</h2>
	<div v-for='chunk in elements_chunks' class='row' style='display: flex;'>
		<div v-for='element in chunk' class='col-sm-3' style='display: flex;'>
			<best-offer :thumb='element.thumb' :subject='element.subject'
						:price='element.price' :expected_price='element.expected_price'
						:mileage='element.mileage' :regdate='element.regdate'
						:economy_pc='element.economy_pc' :id='element.id'>
			</best-offer>
		</div>
	</div>
</div>`,
	data: function() {
		return {
			best_offers: {
				elements: [],
				sample_size: 0,
				available: false
			},
			searching: false
		};
	},
	created: function() {
		var component = this;
		bus.$on('best-offers', function(val) {
			component.best_offers.elements = val.results;
			component.best_offers.sample_size = val.sample_size;
			component.best_offers.available = true;
		});
		bus.$on('searching', function(val) {
			component.searching = val;
			if (component.searching == true)
				component.best_offers.available = false;
		});
	},
	computed: {
		elements_chunks: function() {
			function chunk(array, chunk_size) {
				var i, j, temparray;
				var res = [];
				for (i = 0, j = array.length; i < j; i += chunk_size) {
					temparray = array.slice(i, i + chunk_size);
					res.push(temparray);
				}
				return res;
			}
			return chunk(this.best_offers.elements, 4);
		}
	}
});

var app = new Vue({
	el: '#main'
});
