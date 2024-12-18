<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 mb-4">
    <div class="flex space-x-4">
      <img loading="lazy" :src="reservation.post.images[0]" alt="Item preview" class="w-16 h-16 object-cover rounded-lg"/>
      <div>
        <h3 class="font-medium text-gray-900 dark:text-gray-100">{{ reservation.post.title }}</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">{{ reservation.coins_spent }} coins</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  reservation: {
    type: Object,
    required: true
  }
});
</script>
