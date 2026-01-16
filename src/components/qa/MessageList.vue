<template>
  <div class="message-list-container">
    <div class="message-list-content">
      <MessageItem v-for="message in messages" :key="message.id" :message="message"
        :is-typing="message.role === 'assistant' && message.isTyping" />
    </div>
  </div>
</template>

<script setup>
import { watch, inject } from 'vue' // Import watch for watching data changes, inject for injecting data provided by an ancestor component
import MessageItem from './MessageBU.vue' // Import the message item component (using MessageBU instead of MessageItem)

// Inject the scrollToBottom function provided by an ancestor component (e.g., App.vue or ChatContainer.vue)
// This function is typically used to scroll the chat area to the bottom to display the latest messages
const scrollToBottom = inject('scrollToBottom')

// Define component props, receiving data passed from the parent component
const props = defineProps({
  messages: {
    type: Array, // Array of message objects, containing all chat messages
    required: true, // Required prop
  },
})

// Watch for changes in the props.messages array
// When the messages array changes (e.g., a new message is added), execute the callback function
watch(
  () => props.messages,
  () => {
    // If the scrollToBottom function exists, call it to scroll the chat area to the bottom
    if (scrollToBottom) {
      scrollToBottom()
    }
  },
  {
    deep: true, // Deeply watch for changes within objects inside the messages array
    flush: 'post', // Execute the callback after DOM updates, ensuring proper scrolling position
  },
)
</script>

<style scoped>
/* Styles for the message list container */
.message-list-container {
  flex: 1;
  /* Allow the container to fill available space */
  padding: 10px 0 130px 0;
  /* Inner padding */
  background-color: var(#eee8d5);
  /* Background color using Element Plus theme variable */
  min-height: 0;
  /* 修复flex布局高度计算问题 */
  /* 设置宽度为视口的65%，居中显示 */
  width: 95%;
  margin: 0;
  /* 居中显示 */
  top: 10px;
}

/* Styles for the message list content */
.message-list-content {
  display: flex;
  /* Use Flexbox layout */
  flex-direction: column;
  /* Arrange child elements vertically */
  gap: 20px;
  /* Spacing between message items */
  padding-bottom: 130px;
  /* Leave more space for the input box fixed at the bottom, preventing messages from being obscured */
  background-color: tw-bg-gray-50;
  min-height: 0;
  /* 确保flex布局正确计算 */
  width: 100%;
  max-width: 900px;
  min-width: 0;
}

/* Dark mode styles */
html.dark .message-list-container {
  background-color: #1e1e20 !important;
  /* Dark mode background color */
}
</style>
