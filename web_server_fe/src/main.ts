import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import PrimeVue from "primevue/config";
import "primeflex/primeflex.css";
import "primeicons/primeicons.css";
import "primevue/resources/primevue.min.css";
import "primevue/resources/themes/lara-dark-blue/theme.css";

import Panel from "primevue/panel";
import Button from "primevue/button";
import Dropdown from "primevue/dropdown";
import Card from "primevue/card";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import ProgressSpinner from "primevue/progressspinner";
import Tag from "primevue/tag";

import Tooltip from "primevue/tooltip";

import "./assets/main.css";

const app = createApp(App);

app.use(PrimeVue);
app.component("Panel", Panel);
app.component("Button", Button);
app.component("Dropdown", Dropdown);
app.component("Card", Card);
app.component("Dialog", Dialog);
app.component("InputText", InputText);
app.component("ProgressSpinner", ProgressSpinner);
app.component("Tag", Tag);

app.directive("tooltip", Tooltip);

app.use(createPinia());
app.use(router);

app.mount("#app");
