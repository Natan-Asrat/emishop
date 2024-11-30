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
    wb.value = new Workbox('/service-worker.js');

    // Add event listener for waiting service worker
    wb.value.addEventListener('waiting', () => {
      updateAvailable.value = true;
    });

    // Register the service worker and check for updates every 5 minutes
    wb.value.register().then(() => {
      setInterval(() => {
        wb.value.update();
      }, 5 * 60 * 1000);
    });
  }
});

const updateApp = async () => {
  if (wb.value) {
    // Send message to service worker to skip waiting
    wb.value.messageSkipWaiting();
    // Reload the page to activate the new service worker
    window.location.reload();
  }
};
</script>
