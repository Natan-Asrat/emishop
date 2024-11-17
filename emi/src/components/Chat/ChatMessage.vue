<template>
  <div :class="['flex mb-4', isOwn ? 'justify-end' : 'justify-start']">
    <div :class="['max-w-[70%] rounded-lg p-3', isOwn ? 'bg-blue-500 text-white' : 'bg-gray-100 dark:bg-gray-800']">
      <p class="text-sm">{{ message.content }}</p>
      <span class="text-xs opacity-70">{{ formatDate(message.sent_at) }}</span>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  message: {
    type: Object,
    required: true
  },
  isOwn: {
    type: Boolean,
    default: false
  }
});

const formatDate = (date) => {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};
</script>
