<template>
  <div v-if="isLoading">Loading...</div>
  <div v-else class="main">
    <div class="app" v-if="isAuthenticated">
      <div class="logout">
        <User :user="user" /><button @click="doLogout">Log out</button>
      </div>
      <ChatUI />
    </div>
    <div v-else>
      <button @click="doLogin">Log in</button>
    </div>
  </div>
</template>
<script setup lang="ts">
  import { useAuth0 } from '@auth0/auth0-vue';
  import User from './components/User.vue';
  import ChatUI from './components/ChatUI.vue';

  const { loginWithRedirect, logout, user, isAuthenticated, isLoading } = useAuth0();

  const doLogin = () => { 
    loginWithRedirect();
  };
  const doLogout = () => { 
    logout({ logoutParams: { returnTo: window.location.origin } });
  }
</script>

<style scoped>
.logout {
  display: flex;
  flex-direction: row;
  align-self: flex-end;
}

.app {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.main {
  flex: 1;
  display: flex;
}
</style>