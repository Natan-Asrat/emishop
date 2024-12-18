<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" @close="closeImageSourceDialog" class="relative z-50">
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
              <DialogTitle as="h3" class="text-lg font-medium leading-6 text-white mb-4">
                Choose Image Source
              </DialogTitle>
              <div class="flex space-x-4">
                <button @click="selectImageSource('camera')" class="btn btn-primary flex-1 text-white">
                  <Camera class="h-5 w-5  text-white mx-auto" />
                  Camera
                </button>
                <button @click="selectImageSource('gallery')" class="btn btn-secondary flex-1 text-white">
                  <Image class="h-5 w-5 text-white mx-auto" />
                  Gallery
                </button>
              </div>
              <button @click="closeImageSourceDialog" class="mt-4 text-blue-400 hover:text-blue-300 transition-colors duration-300 text-white">Cancel</button>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { defineProps, defineEmits, watch } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { Camera, Image } from 'lucide-vue-next'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'select-source'])

const closeImageSourceDialog = () => {
  emit('close')
}

const selectImageSource = (source) => {
  emit('select-source', source)
};

</script>
