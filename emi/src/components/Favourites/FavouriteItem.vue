<template>
  <div v-if="product.isActive" class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden product" :data-product-id="product.id" >
    <img loading="lazy" :src="product.image" :alt="product.name" class="w-full h-48 object-cover" @click="openProductDetails(product)" />
    <div class="p-4">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ product.name }}</h2>
      <p class="text-gray-600 dark:text-gray-400 mt-1">
        Price: ${{ new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(product.price) }}
      </p>
      <p class="text-sm text-gray-500 dark:text-gray-500 mt-1">
        Stock: {{ 
          new Intl.NumberFormat('en-US').format(product.stockLeft)  
          }} / {{
            new Intl.NumberFormat('en-US').format(product.totalStock)
          }}
      </p>
      <div class="mt-4 flex items-center justify-between">
        <div class="flex items-center">
          <button
            @click="decrementQuantity(product)"
            class="bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 h-8 w-8 rounded-l"
          >
            -
          </button>
          <input
            type="number"
            :value="product.quantity"
            @input="updateQuantity($event)"
            min="1"
            :max="product.stockLeft"
            class="h-8 w-12 text-center border-t border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300"
          />
          <button
            @click="incrementQuantity()"
            class="bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 h-8 w-8 rounded-r"
          >
            +
          </button>
        </div>
        <button
          @click="reserveProduct()"
          :disabled="isReserving"
          class="bg-indigo-600 text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Reserve
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
const emit = defineEmits(['reserve', 'viewDetails', 'incrementQuantity', 'decrementQuantity', 'updateQuantity']);

const props = defineProps({
  product: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    required: true
  },
  isReserving: {
    type: Boolean,
    required: true,
    default: false
  }
});

const updateQuantity = (event) => {
  const newQuantity = parseInt(event.target.value, 10);
  emit('updateQuantity',props.index, newQuantity );
};

const decrementQuantity = () => {
  emit('decrementQuantity', props.index)
};

const incrementQuantity = () => {
  emit('incrementQuantity', props.index)
};

const reserveProduct = async () => {
  if(props.isReserving) return
  emit('reserve', props.product);
};

const openProductDetails = () => {
  emit('viewDetails', props.product);
};
</script>
