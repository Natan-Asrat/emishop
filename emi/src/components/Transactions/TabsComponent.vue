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
        <span v-if="trueForReservationFalseForOrder && transactionStore.reservationsCount != null" class="mr-1 inline-block w-5 h-5 rounded-full text-white dark:text-black" :class="{ 'bg-blue-600 dark:bg-blue-400': tab.toLowerCase() === 'pending', 'bg-green-600 dark:bg-green-400': tab.toLowerCase() === 'completed', 'bg-red-600 dark:bg-red-400': tab.toLowerCase() === 'cancelled' }">{{ transactionStore.reservationsCount[tab.toLowerCase()] }} </span>
        <span v-if="!trueForReservationFalseForOrder && transactionStore.ordersCount != null" class="mr-1 inline-block w-5 h-5 rounded-full  text-white dark:text-black" :class="{ 'bg-blue-600 dark:bg-blue-400': tab.toLowerCase() === 'pending', 'bg-green-600 dark:bg-green-400': tab.toLowerCase() === 'completed', 'bg-red-600 dark:bg-red-400': tab.toLowerCase() === 'cancelled' }">{{ transactionStore.ordersCount[tab.toLowerCase()] }}</span>
         {{ tab }}
      </button>
      </div>
    </div>
</template>
<script setup>
import { defineProps, defineEmits } from 'vue'
import { useTransactionsStore } from '@/stores/transactions';
const transactionStore = useTransactionsStore();
const tabs = ['Pending', 'Completed', 'Cancelled'];

defineProps({
  currentTab: {
    type: String,
    required: true
  },
  trueForReservationFalseForOrder: {
    type: Boolean,
    required: true
  }
})
const emit = defineEmits(['setCurrentTab']);

const setCurrentTab = (tab) => {
  emit('setCurrentTab', tab)
}
</script>
