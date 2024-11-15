<template>
  <div ref="recentlyViewed" class="bg-white dark:bg-gray-800 shadow-inner overflow-hidden">
    <div class="py-4">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3 px-4">Recently Viewed</h2>
      <div class="flex overflow-x-auto space-x-4 pb-4 scrollbar-hide px-4">
        <div v-for="product in recentProducts" :key="product.id" class="flex-shrink-0" >
          <div class="w-20 h-20 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden">
            <img :src="product.image" :alt="product.name" class="w-full h-full object-cover" />
          </div>
          <p class="mt-2 text-xs text-center text-gray-600 dark:text-gray-400">{{ product.name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
const recentlyViewed = ref(null)

const recentProducts = ref([
    { id: 1, name: 'Product 1', image: 'https://placehold.co/80' },
    { id: 2, name: 'Product 2', image: 'https://placehold.co/80' },
    { id: 3, name: 'Product 3', image: 'https://placehold.co/80' },
    { id: 4, name: 'Product 4', image: 'https://placehold.co/80' },
    { id: 5, name: 'Product 5', image: 'https://placehold.co/80' },
    { id: 6, name: 'Product 6', image: 'https://placehold.co/80' },
    { id: 7, name: 'Product 7', image: 'https://placehold.co/80' },
    { id: 8, name: 'Product 8', image: 'https://placehold.co/80' },
  ])
</script>
