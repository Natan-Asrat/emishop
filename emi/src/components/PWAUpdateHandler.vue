<template>
  <div v-if="updateAvailable" class="fixed bottom-4 right-4 z-50 bg-blue-600 text-white p-4 rounded-lg shadow-lg flex items-center space-x-4">
    <span>New version available!</span>
    <button @click="updateApp" class="px-4 py-2 bg-white text-blue-600 rounded hover:bg-blue-50">
      Update now
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Workbox } from 'workbox-window';

const updateAvailable = ref(false);
const wb = ref(null);

onMounted(() => {
  if ('serviceWorker' in navigator) {
    wb.value = new Workbox('/sw.js');

    wb.value.addEventListener('waiting', (event) => {
      console.log('A new service worker is waiting to be activated');
      updateAvailable.value = true;
    });

    wb.value.addEventListener('controlling', () => {
      console.log('A new service worker is now controlling the page');
      window.location.reload();
    });

    wb.value.addEventListener('activated', (event) => {
      console.log('Service worker activated');
    });

    wb.value.register().then((registration) => {
      console.log('Service Worker registered');
      
      setInterval(() => {
        console.log('Checking for updates...');
        wb.value.update();
      }, 5 * 60 * 1000);
    }).catch((error) => {
      console.error('Service Worker registration failed:', error);
    });
  }
});

const updateApp = async () => {
  if (wb.value) {
    console.log('Sending skip waiting message to service worker');
    wb.value.messageSkipWaiting();
  }
};
</script>
