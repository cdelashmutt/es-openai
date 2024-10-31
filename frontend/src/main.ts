import { createAuth0 } from '@auth0/auth0-vue';

import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

const app = createApp(App);

app.use(
  createAuth0({
    domain: 'dev-qwxg0cfmxcub4nih.us.auth0.com',
    clientId: 'wqIfAjUc5xNj8P1fjc5n0U53ZmvZSCb5',
    authorizationParams: {
      redirect_uri: window.location.origin
    }
  })
);

app.mount('#app');

