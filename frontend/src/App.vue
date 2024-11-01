<template>
  <div v-if="isLoading">Loading...</div>
  <div v-else>
    <div class="logout" v-if="isAuthenticated">
      <User :user="user" /><button @click="doLogout">Log out</button>
    </div>
    <div v-else>
      <button @click="doLogin">Log in</button>
    </div>
  </div>
</template>
<script setup>
  import { useAuth0, Auth0VueClient } from '@auth0/auth0-vue';
  import User from './components/User.vue';
  const auth0Client = useAuth0();

  const doLogin = () => { 
    auth0 = loginWithRedirect();
  };
  const doLogout = () => { 
    auth0 = logout({ logoutParams: { returnTo: window.location.origin } });
  }
</script>
<style>
.logout {
  display: flex;
  flex-direction: row;
}
</style>