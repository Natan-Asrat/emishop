<template>
  <main ref="mainContent" class="pb-20">
    <div class="px-4 py-6 space-y-6 overflow-y-auto" style="margin-top: 265px">
      <FeedItem
        v-for="product in products"
        :key="product.id"
        :product="product"
        @viewDetails="openProductDetails"
        @reserve="reserveProduct"
      />
    </div>
  </main>
</template>
<script setup>
import { ref } from 'vue'
import FeedItem from './FeedItem.vue';
const products = ref([
    {
      id: 1,
      name: "Stylish Watch",
      price: 199.99,
      image: "https://placehold.co/300",
      images: [
        "https://placehold.co/300",
        "https://placehold.co/300",
        "https://placehold.co/300"
      ],
      stockLeft: 5,
      totalStock: 10,
      quantity: 1,
      description: "A sleek and modern watch that combines style with functionality.",
      sellerName: "John Doe",
      sellerAvatar: "https://placehold.co/40",
      postedDate: "2023-05-15"
    },
    {
      id: 2,
      name: "Wireless Earbuds",
      price: 89.99,
      image: "https://placehold.co/300",
      images: [
        "https://placehold.co/300",
        "https://placehold.co/300",
        "https://placehold.co/300"
      ],
      stockLeft: 8,
      totalStock: 15,
      quantity: 1,
      description: "High-quality wireless earbuds with noise-cancelling technology.",
      sellerName: "Jane Smith",
      sellerAvatar: "https://placehold.co/40",
      postedDate: "2023-05-14"
    },
    {
      id: 3,
      name: "Smart Home Speaker",
      price: 129.99,
      image: "https://placehold.co/300",
      images: [
        "https://placehold.co/300",
        "https://placehold.co/300",
        "https://placehold.co/300"
      ],
      stockLeft: 3,
      totalStock: 8,
      quantity: 1,
      description: "A powerful smart speaker with voice control and excellent sound quality.",
      sellerName: "Mike Johnson",
      sellerAvatar: "https://placehold.co/40",
      postedDate: "2023-05-13"
    },
  ])
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
