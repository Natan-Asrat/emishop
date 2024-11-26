<template>
  <div class="flex border-b dark:border-gray-700 p-4 items-center">
    <router-link
        :to="{'name': 'home'}"
        class="p-2 mr-2 rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        aria-label="Notifications"
      >
        <ArrowLeft class="h-6 w-6" />
      </router-link>
    <h2 class="text-xl text-center font-semibold text-gray-900 dark:text-gray-100">
      Chat with {{ recipientName }}
    </h2>
  </div>
</template>
<script setup>
import { ArrowLeft } from 'lucide-vue-next';
defineProps({
  recipientName: {
    type: String,
    required: false
  }
})
</script>
