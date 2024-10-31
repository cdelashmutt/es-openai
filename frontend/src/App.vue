<template>
  <Login :isAuthenticated="isAuthenticated"/>
</template>
<script setup>
  import { ref } from 'vue';
  import Login from './components/Login.vue'

  const isAuthenticated=ref(false);

</script>