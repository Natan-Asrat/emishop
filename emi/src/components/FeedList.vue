<template>
  <main ref="mainContent" class=" pb-20">
    <!-- Vertically Scrollable Product Feed -->
    <div class="px-4 py-6 space-y-6 overflow-y-auto h-[calc(100vh-8rem)]">
      <div v-for="product in products" :key="product.id" class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden product" :data-product-id="product.id" >
        <img :src="product.image" :alt="product.name" class="w-full h-48 object-cover" @click="openProductDetails(product)" />
        <div class="p-4">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ product.name }}</h2>
          <p class="text-gray-600 dark:text-gray-400 mt-1">Price: ${{ product.price.toFixed(2) }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-500 mt-1">
            Stock: {{ product.stockLeft }} / {{ product.totalStock }}
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
                v-model.number="product.quantity"
                min="1"
                :max="product.stockLeft"
                class="h-8 w-12 text-center border-t border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300"
              />
              <button
                @click="incrementQuantity(product)"
                class="bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 h-8 w-8 rounded-r"
              >
                +
              </button>
            </div>
            <button
              @click="reserveProduct(product)"
              class="bg-indigo-600 text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Reserve
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>
import { ref } from 'vue'
const products = ref([])
const selectedProduct = ref(null)
const isReserving = ref(false);
const requiredCoins = ref(0)
const postInteractions = ref({})

const openProductDetails = (product) => {
  selectedProduct.value = product
  updatePostInteraction(product.id, 'detailView')
  const startTime = Date.now()
  product.startViewTime = startTime
}

const decrementQuantity = (product) => {
  if (product.quantity > 1) {
    product.quantity--
  }
}
const incrementQuantity = (product) => {
  if (product.quantity < product.stockLeft) {
    product.quantity++
  }
}

const closeProductDetails = () => {
  if (selectedProduct.value) {
    const endTime = Date.now()
    const timeSpent = (endTime - selectedProduct.value.startViewTime) / 1000 // Convert to seconds
    console.log(`Time spent on product ${selectedProduct.value.id}: ${timeSpent} seconds`)
    updateInteractionTime(selectedProduct.value.id, timeSpent)
  }
  selectedProduct.value = null
}
const updateInteractionTime = (postId, time) => {
  if (!interactionTimes.value[postId]) {
    interactionTimes.value[postId] = 0
  }
  interactionTimes.value[postId] += time
  console.log(`Total time on ${postId}: ${interactionTimes.value[postId]}` )

}
const updatePostInteraction = (postId, interactionType, quantity = 1) => {
  if (!postInteractions.value[postId]) {
    postInteractions.value[postId] = 0
  }
  const interaction = INTERACTION_WEIGHTS[interactionType] * quantity
  postInteractions.value[postId] += interaction
}
const reserveProduct = async (product) => {
  console.log("prod", product)
  const requiredCoins = Math.ceil(product.price * 0.01 * product.quantity);

  if (userCoins.value < requiredCoins) {
    requiredCoins.value = requiredCoins;
    showInsufficientCoinsModal.value = true;
    return;
  }

  try {
    isReserving.value = true;

    const response = await reservationApi.createReservation(product.id, product.quantity);

    // Update local state
    userCoins.value -= requiredCoins;
    product.stockLeft -= product.quantity;
    updatePostInteraction(product.id, 'reserve', product.quantity);

    // Close product details if open
    closeProductDetails();

    // Subscribe to WebSocket updates for this reservation
    // websocketService.subscribe('notification', handleReservationNotification);

    // Navigate to transactions page
    router.push('/transactions');

  } catch (error) {
    console.error('Error creating reservation:', error);
    if (error.response?.data?.error === 'Insufficient coins') {
      requiredCoins.value = requiredCoins;
      showInsufficientCoinsModal.value = true;
    } else if (error.response?.data?.error === 'Insufficient stock') {
      alert('This item is out of stock or quantity not available');
    } else {
      alert('Failed to reserve the item. Please try again.');
    }
  } finally {
    isReserving.value = false;
  }
};
</script>
