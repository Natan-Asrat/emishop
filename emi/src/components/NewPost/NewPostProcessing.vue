<template>
  <TransitionRoot appear :show="isProcessing" as="template">
    <Dialog as="div" @close="isProcessing = false" class="relative z-50">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-25 backdrop-blur-sm" />
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
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-gray-900 p-6 text-left align-middle shadow-xl transition-all">
              <div class="flex flex-col items-center">
                <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mb-4"></div>
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-white">
                  Processing Tags
                </DialogTitle>
                <p class="mt-2 text-sm text-gray-400">
                  Please wait while we generate embeddings for your tags...
                </p>
                <p class="mt-2 text-sm text-gray-400">
                  {{ progress }}
                </p>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
<script setup>
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
defineProps({
  isProcessing: {
    type: Boolean,
    required: true
  },
  progress: {
    type: String,
    required: true
  }
})
</script>
