<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import Sidebar from './Sidebar.vue';
import ChatWindow from './ChatWindow.vue';
import { Conversation, Message, SenderType } from '../types';

const conversations = ref(<Array<Conversation>> new Array());

onMounted(() => {
  conversations.value = JSON.parse(localStorage.getItem('conversations') || "");
  if(!conversations.value) {
    const conversation: Conversation = {id: Date.now(), title: 'First Conversation', messages: [] }
    conversations.value = [conversation]
  }
  selectConversation(conversations.value[0]);
});

watch (conversations, (newConversations) => {
  localStorage.setItem("conversations", JSON.stringify(newConversations));
}, {deep: true});

const selectedConversation = ref<Conversation>(conversations.value[0]);

function selectConversation(conversation: Conversation) {
  selectedConversation.value = conversation;
}

let eventSource: EventSource | null = null;

function sendMessage(message: string) {
  const messObj: Message = { text: message, sender: SenderType.user };
  selectedConversation.value.messages.push(messObj);
  if(!eventSource && message) {
    eventSource = new EventSource(`/ai/generate?chatId=${encodeURIComponent(selectedConversation.value.id)}&message=${encodeURIComponent(message)}`);

    const messageIndex = selectedConversation.value.messages.length;
    selectedConversation.value.messages.push({ text: "", sender: SenderType.system });

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const content = data.result.output.content;

        selectedConversation.value.messages[messageIndex].text += content;
      } catch (e) {
        console.error("Error parsing event data: ", e);
      }
    };

    console.log("SSE Stream opened with message:", message);
  } else {
    console.log("No message to send, so skipping stream open.");
  }
}

function closeStream() {
  if(eventSource) {
    eventSource.close();
    eventSource = null;
  }
}

onUnmounted(() => {
  closeStream();
});

function createConversation() {
  const newConversation = {
    id: Date.now(),
    title: `Conversation ${conversations.value.length + 1}`,
    messages: []
  }
  conversations.value.push(newConversation);
  selectConversation(newConversation);
}

function deleteConversation(conversationToDelete: Conversation) {
  conversations.value = conversations.value.filter(
    conversation => conversation.id !== conversationToDelete.id
  );
  if (selectedConversation.value.id === conversationToDelete.id) {
    selectConversation(conversations.value[0] || null);
  }
}
const selectedMessages = computed(() => selectedConversation.value?.messages);
</script>

<template>
  <div class="chat-ui">
    <Sidebar
      :conversations="conversations"
      :selectedConversation="selectedConversation"
      @selectConversation="selectConversation"
      @createConversation="createConversation"
      @deleteConversation="deleteConversation" />
    <ChatWindow :messages="selectedMessages" @sendMessage="sendMessage" />
  </div>
</template>

<style scoped>
.chat-ui {
  display: flex;
  height: 85vh;
}
</style>