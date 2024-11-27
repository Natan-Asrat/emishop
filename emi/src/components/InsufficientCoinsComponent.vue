<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl max-w-sm w-full mx-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Insufficient Coins</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-4">
            This product requires {{ requiredCoins }} coins to reserve. You currently have {{ userCoins }} coins.
          </p>
          <div class="flex justify-end">
            <button
              @click="closeInsufficientCoinsModal"
              class="bg-gray-300 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-md mr-2 hover:bg-gray-400 dark:hover:bg-gray-600"
            >
              Close
            </button>
            <button
              @click="redirectToBuyCoins"
              class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Buy Coins
            </button>
          </div>
        </div>
      </div>
</template>
<script setup>
defineProps({
  requiredCoins: {
    type: Number,
    required: true
  },
  userCoins: {
    type: Number,
    required: true
  }
})
const emit = defineEmits(['closeInsufficientCoinsModal'])

const closeInsufficientCoinsModal = () => {
  emit('closeInsufficientCoinsModal')
}

const redirectToBuyCoins = () => {

}

</script>
