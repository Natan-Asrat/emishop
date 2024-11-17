<template>
  <div class="border-b dark:border-gray-700 p-4">
    <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100">
      Chat with {{ recipientName }}
    </h2>
  </div>
</template>
<script setup>
defineProps({
  recipientName: {
    type: String,
    required: false
  }
})
</script>
