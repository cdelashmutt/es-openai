<script setup lang="ts">
import { Conversation } from '../types';

defineProps<{
  conversations?: Array<Conversation>,
  selectedConversation?: Conversation,
}>();
</script>

<template>
  <aside class="sidebar">
    <button class="new-conversation-btn" @click="$emit('createConversation')">New Conversation</button>
    <ul>
      <li
        v-for="conversation in conversations"
        :key="conversation.id"
        :class="{active: conversation.id === selectedConversation?.id}"
      >
        <span @click="$emit('selectConversation', conversation)" class="conversation-title">
          {{ conversation.title }}
        </span>
        <span class="delete" @click="$emit('deleteConversation', conversation)">🗑️</span>
      </li>
    </ul>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 200px;
  background-color: #f1f1f1;
  padding: 1rem;
}

ul {
  list-style: none;
  padding: 0;
  flex-grow: 1;
}

.conversation-title {
  cursor: pointer;
  flex-grow: 1;
}

li {
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

li.active {
  font-weight: bold;
  background-color: #ddd;
}

.delete {
  font-size: 1.2rem;
  cursor: pointer;
  align-self: center;
}
</style>