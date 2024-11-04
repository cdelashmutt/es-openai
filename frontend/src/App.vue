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
<script setup lang="ts">
  import { useAuth0 } from '@auth0/auth0-vue';
  import User from './components/User.vue';
  const { loginWithRedirect, logout, user, isAuthenticated, isLoading } = useAuth0();

  const doLogin = () => { 
    loginWithRedirect();
  };
  const doLogout = () => { 
    logout({ logoutParams: { returnTo: window.location.origin } });
  }
</script>
<style>
.logout {
  display: flex;
  flex-direction: row;
}
</style>