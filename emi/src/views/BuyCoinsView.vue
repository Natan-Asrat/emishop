<template>
  <main class="min-h-screen bg-gray-200 dark:bg-gray-600 pb-20 pt-12">
    <div class="px-4 relative">
      <span class="absolute text-gray-700 dark:text-gray-200 text-sm right-6">Coins: {{ userStore.user.coins }}</span>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">Buy Coins</h1>
      <div class="grid grid-cols-2 gap-4 md:grid-cols-3">
        <div v-for="(option, index) in coinOptions" :key="option.coins" 
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
          <div class="p-4">
            <div class="flex justify-center mb-3">
              <img loading="lazy" :src="option.image" alt="Coin" class="w-16 h-16"/>
            </div>
            <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 text-center">
              {{ option.coins }} {{ option.coins === 1 ? 'Coin' : 'Coins' }}
            </h2>
            <p class="text-gray-600 dark:text-gray-400 mt-1 text-center">${{ option.price.toFixed(2) }}</p>
            <button 
              @click="handlePayment(option, index)"
              class="w-full mt-3 bg-indigo-600 text-white px-4 py-2 rounded-full text-sm font-medium 
                hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              :disabled="isLoading && loadingIndex === index"
            >
              <span v-if="!isLoading || loadingIndex !== index">Buy Now</span>
              <span v-else class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Loading...
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" 
         id="paypal-modal" 
         style="display: none;">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl max-w-md w-full mx-auto relative">
        <div class="max-h-[80vh] overflow-y-auto">
          <div id="paypal-button-container" class="w-full"></div>
          <button 
            @click="closePayPalModal"
            class="mt-4 w-full bg-gray-500 text-white px-4 py-2 rounded-full text-sm font-medium 
              hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </main>
  <FooterComponent />
</template>

<script setup>
import { onMounted, ref } from 'vue';
import FooterComponent from '@/components/FooterComponent.vue';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import {useRouter} from 'vue-router';
import onecoin from '@/assets/onecoin.png';
import threecoins from '@/assets/threecoins.png';
import tencoins from '@/assets/tencoins.png';
import twentyfivecoins from '@/assets/twentyfivecoins.png';
import hundredcoins from '@/assets/hundredcoins.png';
import twothousandcoins from '@/assets/twothousandcoins.png';

const toastStore = useToastStore();
const userStore = useUserStore();
const isLoading = ref(false);
const router = useRouter();
const loadingIndex = ref(null);

const coinOptions = [
  { coins: 1, price: 1, image: onecoin},
  { coins: 3, price: 3, image: threecoins},
  { coins: 10, price: 10, image: tencoins },
  { coins: 25, price: 25, image: twentyfivecoins },
  { coins: 100, price: 100, image: hundredcoins },
  { coins: 2000, price: 2000, image: twothousandcoins }
];

let paypal;

onMounted(() => {
  const script = document.createElement('script');
  script.src = `https://www.paypal.com/sdk/js?client-id=${import.meta.env.VITE_PAYPAL_CLIENT_ID}&currency=USD`;
  script.addEventListener('load', initializePayPal);
  document.body.appendChild(script);
});

function initializePayPal() {
  paypal = window.paypal;
}

function closePayPalModal() {
  const modal = document.getElementById('paypal-modal');
  modal.style.display = 'none';
  isLoading.value = false;
  loadingIndex.value = null;
}

async function handlePayment(option, index) {
  try {
    isLoading.value = true;
    loadingIndex.value = index;
    
    // Create PayPal order through our backend
    const { data: orderData } = await axios.post('/api/account/create-paypal-order/', {
      coins: option.coins,
      price: option.price.toFixed(2)  // Ensure price is properly formatted
    });

    if (!orderData.id) {
      throw new Error('Failed to create PayPal order');
    }

    const paypalButtons = paypal.Buttons({
      createOrder: () => orderData.id,
      onApprove: async (data) => {
        try {
          // Capture the payment through our backend
          const { data: captureData } = await axios.post('/api/account/capture-paypal-order/', {
            orderId: data.orderID
          });

          if (captureData.success) {
            // Update user's coins in the store
            await userStore.refreshCoins();
            router.push({name: 'myprofile'})
            
            // Hide PayPal modal
            closePayPalModal();
          } else {
            throw new Error('Payment capture failed');
          }
        } catch (error) {
          console.error('Payment capture error:', error);
          loadingIndex.value = null;
        }
      },
      onError: (err) => {
        console.error('PayPal error:', err);
        isLoading.value = false;
        loadingIndex.value = null;
      },
      onCancel: () => {
        closePayPalModal();
      }
    });

    const container = document.getElementById('paypal-button-container');
    container.innerHTML = '';
    await paypalButtons.render('#paypal-button-container');
    
    // Show the modal
    const modal = document.getElementById('paypal-modal');
    modal.style.display = 'flex';
    isLoading.value = false;
    loadingIndex.value = null;
  } catch (error) {
    console.error('Payment initialization error:', error);
    isLoading.value = false;
    loadingIndex.value = null;
  }
}
</script>
