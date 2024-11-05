<template>
  <div class="chat-window">
    <div class="messages" ref="chatWindow" @scroll="handleScroll">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message-card', message.sender]"
      >
        {{ message.text }}
      </div>
    </div>
    <div class="input-box">
      <span class="paperclip">📎</span>
      <input type="text" v-model="newMessage" placeholder="Type a message..." @keyup.enter="send" />
      <button @click="send">Send</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick, useTemplateRef } from 'vue';
import { Message } from '../types';

const props = defineProps({
  messages: Array<Message>,
});

const emit = defineEmits(['sendMessage']);

const chatWindow = useTemplateRef('chatWindow');
const newMessage = ref("");
const autoScrollEnabled = ref(true);

function send() {
  if (newMessage.value.trim()) {
    emit("sendMessage", newMessage.value.trim());
    newMessage.value = "";
    scrollToBottom();
  }
}

function handleScroll() {
  if(chatWindow) {
    const { scrollTop, scrollHeight, clientHeight } = chatWindow.value as HTMLDivElement;
    const isAtBottom = scrollTop + clientHeight >= scrollHeight - 10; // Within 10px of the bottom
    autoScrollEnabled.value = isAtBottom;
  }
}

watch(
  () => props.messages?.map(msg => msg.text),
  async () => {
    if (autoScrollEnabled.value) {
      await scrollToBottom();
    }
  },
  { deep: true }
);

async function scrollToBottom() {
  await nextTick();
  if(chatWindow?.value?.scrollTop) {
    chatWindow.value.scrollTop = chatWindow?.value.scrollHeight;
  }
}

onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  overflow-y: auto;
  background-color: #fff;
}

.message-card {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border-radius: 5px;
}

.message-card.user {
  background-color: #d1e7dd;
  align-self: flex-end;
}

.message-card.system {
  background-color: #f8d7da;
  align-self: flex-start;
  white-space: pre-wrap;
}

.input-box {
  display: flex;
  padding: 0.5rem;
  background-color: #f1f1f1;
}

.input-box input {
  flex: 1;
  padding: 0.5rem;
  margin: 0 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.input-box button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.input-box .paperclip {
  font-size: 1.2rem;
  cursor: pointer;
  align-self: center;
}
</style>