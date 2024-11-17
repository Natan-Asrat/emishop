<template>
  <div class="mb-6">
      <div class="flex space-x-1 rounded-xl bg-gray-200 dark:bg-gray-800 p-1">
        <button
        v-for="tab in tabs"
        :key="tab"
        @click="setCurrentTab(tab)"
        :class="[
          'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
          'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
          currentTab === tab
          ? 'bg-white dark:bg-gray-700 shadow text-blue-700 dark:text-blue-200'
          : 'text-gray-700 dark:text-gray-300 hover:bg-white/[0.12] hover:text-blue-700 dark:hover:text-blue-200'
        ]">
        {{ tab }}
      </button>
      </div>
    </div>
</template>
<script setup>
import { defineProps, defineEmits } from 'vue'
const tabs = ['Favourites', 'Pending', 'Purchased'];

defineProps({
  currentTab: {
    type: String,
    required: true
  }
})
const emit = defineEmits(['setCurrentTab']);

const setCurrentTab = (tab) => {
  emit('setCurrentTab', tab)
}
</script>
