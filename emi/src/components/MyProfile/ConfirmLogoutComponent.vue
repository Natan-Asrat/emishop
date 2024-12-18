<template>
  <TransitionRoot appear :show="true" as="template">
    <Dialog as="div" @close="closeModal" class="relative z-50">
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
                <!-- <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mb-4"></div> -->
                <div v-if="user?.avatar" class="mb-5">
                  <img loading="lazy" :src="user.avatar" :alt="user.name" class="w-24 h-24 rounded-full object-cover"/>

                </div>
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-white text-center">
                  @{{user.username}}
                </DialogTitle>
                <p class="mt-2 text-sm text-gray-400 text-center">
                  {{ user.name }}
                </p>
                <div class="flex mt-4 gap-4 w-full">
                  <button @click="closeModal" class="py-2 px-6 flex-grow bg-yellow-200 text-black rounded-lg">Cancel</button>
                  <button @click="logout" class="py-2 px-6 flex-grow bg-red-700 text-gray-100 rounded-lg">Logout</button>

                </div>
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
  user: {
    type: Object,
    required: true
  }
})
const emit = defineEmits(['closeModal', 'logout'])
const closeModal = () => {
  emit('closeModal')
}
const logout = () => {
  emit('logout')
}
</script>
