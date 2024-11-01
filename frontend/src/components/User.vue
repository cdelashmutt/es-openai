<template>
  <div class="user-image">
    <div class="user-image-frame"><img :src="user.picture" /></div>
    <div class="name">{{ user.name }}</div>
  </div>
</template>
<script setup lang="ts">
defineProps<{user?: object}>();

</script>
<style>
.user-image {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.user-image-frame {
  border: 2px solid #c7b89e;

}
.user-image-frame, .user-image-frame img {
  width: 50px;
  height: 50px;
  border-radius: 30px;
}
.name {
  margin: 5px;
}
</style>