<template>
  <transition name="slide-up">
    <div v-if="selectedProduct" class="fixed inset-0 bg-black bg-opacity-50 flex items-end justify-center z-40">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-t-3xl shadow-xl w-full max-h-[90vh] overflow-y-auto">
        <button @click="closeProductDetails" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
          <XIcon class="h-6 w-6 text-white" />
        </button>
        <div class="mb-4 relative">
          <swiper
            :modules="swiperModules"
            :pagination="{ clickable: true }"
            class="h-64 w-full rounded-lg"
          >
            <swiper-slide v-for="(image, index) in selectedProduct.images" :key="index">
              <img loading="lazy" :src="image" :alt="`${selectedProduct.name} - Image ${index + 1}`" class="w-full h-full object-cover" />
            </swiper-slide>
          </swiper>
        </div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">{{ selectedProduct.name }}</h2>
        <p class="text-gray-600 dark:text-gray-400 mb-4">{{ selectedProduct.description }}</p>
        <p class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">Price: ${{ selectedProduct.price.toFixed(2) }}</p>
        <p class="text-sm text-gray-500 dark:text-gray-500 mb-4">Stock: {{ selectedProduct.stockLeft }} / {{ selectedProduct.totalStock }}</p>
        <div class="flex items-center mb-4">
          <img loading="lazy" :src="selectedProduct.sellerAvatar" alt="Seller Avatar" class="w-10 h-10 rounded-full mr-3" />
          <div>
            <p class="font-semibold text-gray-900 dark:text-gray-100">{{ selectedProduct.sellerName }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-500">Posted on {{ selectedProduct.postedDate }}</p>
          </div>
        </div>
        <button
          @click="reserveProduct(selectedProduct)"
          :disabled="isReserving"
          class="bg-indigo-600 text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {{ isReserving ? 'Reserving...' : 'Reserve' }}
        </button>
      </div>
    </div>
  </transition>
</template>
<script setup>
import {XIcon} from 'lucide-vue-next'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
const swiperModules = [Pagination]

defineProps({
  selectedProduct: {
    type: Object,
    required: true
  },
  isReserving: {
    type: Boolean,
    default: false,
    required: true
  }
})
const emit = defineEmits(['closeProductDetails','reserveProduct'])
const closeProductDetails = () => {
  emit('closeProductDetails')
}
const reserveProduct = (product) => {
  if(props.isReserving) return
  emit('reserveProduct', product)
}
</script>
