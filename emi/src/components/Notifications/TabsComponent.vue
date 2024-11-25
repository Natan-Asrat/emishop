<template>
  <div class="mb-6">
      <div class="mb-1 flex space-x-1 rounded-xl bg-gray-200 dark:bg-gray-800 p-1">
        <button
        @click="setCurrentTab('All')"
        :class="[
          'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
          'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
          currentTab === 'All'
          ? 'bg-white dark:bg-gray-700 shadow text-blue-700 dark:text-blue-200'
          : 'text-gray-700 dark:text-gray-300 hover:bg-white/[0.12] hover:text-blue-700 dark:hover:text-blue-200'
        ]">
        <span v-if=" notificationStore.count != null" class="mr-1 inline-block w-5 h-5 rounded-full bg-black text-white">{{ notificationStore.count['all'] }} </span>
         All
      </button>
      </div>
      <div class="flex space-x-1 rounded-xl bg-gray-200 dark:bg-gray-800 p-1">

        <button
        v-for="tab in tabs.filter(t => t !== 'All')"
        :key="tab"
        @click="setCurrentTab(tab)"
        :class="[
          'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
          'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
          currentTab === tab
          ? 'bg-white dark:bg-gray-700 shadow text-blue-700 dark:text-blue-200'
          : 'text-gray-700 dark:text-gray-300 hover:bg-white/[0.12] hover:text-blue-700 dark:hover:text-blue-200'
        ]">
        <span v-if=" notificationStore.count != null" class="mr-1 inline-block w-5 h-5 rounded-full" :class="{ ' bg-black text-white': tab.toLowerCase() === 'all', 'bg-blue-600 dark:bg-blue-400 text-black': tab.toLowerCase() === 'messages', 'bg-green-600 dark:bg-green-400 text-black': tab.toLowerCase() === 'reservations', 'bg-purple-600 dark:bg-purple-400 text-black': tab.toLowerCase() === 'posts' }">{{ notificationStore.count[tab.toLowerCase()] }} </span>
         {{ tab }}
      </button>
      </div>
    </div>
</template>
<script setup>
import { defineProps, defineEmits } from 'vue'
import { useNotificationStore } from '@/stores/notification';
const notificationStore = useNotificationStore();
const tabs = ['All', 'Reservations', 'Posts', 'Messages'];

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
