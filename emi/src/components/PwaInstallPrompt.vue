<template>
  <div>
    <div v-if="showPrompt" @click="isModalOpen = true" class="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-2 text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700">
      <p class="text-sm font-medium text-gray-700 dark:text-gray-300">Install this app for a better experience!</p>
    </div>

    <TransitionRoot appear :show="isModalOpen" as="template">
      <Dialog as="div" @close="isModalOpen = false" class="relative z-50">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 p-6 text-left align-middle shadow-xl transition-all">
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 dark:text-white text-center mb-4">
                  Choose Installation Method
                </DialogTitle>
                
                <div class="grid grid-cols-2 gap-4 mb-4">
                  <a href="#" class="flex flex-col items-center p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    <img src="/appstore.png" alt="App Store" class="w-16 h-16 mb-2">
                    <span class="text-sm font-medium text-gray-700 dark:text-gray-300">App Store</span>
                  </a>
                  <a href="#" class="flex flex-col items-center p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    <img src="/playstore.png" alt="Play Store" class="w-16 h-16 mb-2">
                    <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Play Store</span>
                  </a>
                </div>

                <div class="mt-4">
                  <button
                    type="button"
                    class="w-full inline-flex justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2"
                    @click="installPwa"
                  >
                    Install Directly
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue'

const showPrompt = ref(false)
const isModalOpen = ref(false)
let deferredPrompt = null

onMounted(() => {
  window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault()
    deferredPrompt = event
    showPrompt.value = true
  })
})

const installPwa = async () => {
  if (!deferredPrompt) return
  
  isModalOpen.value = false
  deferredPrompt.prompt()
  const { outcome } = await deferredPrompt.userChoice
  
  if (outcome === 'accepted') {
    console.log('User accepted the PWA installation')
  } else {
    console.log('User dismissed the PWA installation')
  }
  
  deferredPrompt = null
  showPrompt.value = false
}
</script>
