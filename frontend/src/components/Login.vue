<template>
  <div v-if="isLoading">Loading...</div>
  <div v-else>
    <div v-if="isAuthenticated">
      <button @click="doLogout">Log out</button>
    </div>
    <div v-else>
      <button @click="doLogin">Log in</button>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { useAuth0 } from '@auth0/auth0-vue';
  defineProps<{ isAuthenticated }>()
  const { loginWithRedirect, logout, user, isAuthenticated, isLoading } = useAuth0();

  const doLogin = () => { 
    loginWithRedirect();
  };
  const doLogout = () => { 
    logout({ logoutParams: { returnTo: window.location.origin } });
  }
</script>
<style>
</style>