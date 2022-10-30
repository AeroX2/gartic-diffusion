import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config';
// import 'primevue/resources/primevue.min.css'
// import 'primevue/resources/themes/lara-dark-blue/theme.css'
// import 'primeicons/primeicons.css' 

import Panel from 'primevue/panel'
import Toolbar from 'primevue/toolbar'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import AutoComplete from 'primevue/autocomplete'
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
import Inplace from 'primevue/inplace'
import InputText from 'primevue/inputtext'
import Editor from 'primevue/editor'
import Chips from 'primevue/chips'

import Tooltip from 'primevue/tooltip'

import './assets/main.css'

const app = createApp(App)

app.use(PrimeVue);
app.component('Panel', Panel)
app.component('Toolbar', Toolbar)
app.component('Button', Button)
app.component('Dropdown', Dropdown)
app.component('AutoComplete', AutoComplete)
app.component('Card', Card)
app.component('Tag', Tag)
app.component('Dialog', Dialog)
app.component('Inplace', Inplace)
app.component('InputText', InputText)
app.component('Editor', Editor)
app.component('Chips', Chips)

app.directive('tooltip', Tooltip)

app.use(createPinia())
app.use(router)

app.mount('#app')
